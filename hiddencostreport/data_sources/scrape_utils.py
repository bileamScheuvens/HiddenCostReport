import base64
import asyncio
from asyncio import TaskGroup
from tqdm import tqdm
from time import time
from ..constants import DATADIR, ROOT, CURATEDMETRICPATHS
import os
import numpy as np
import pandas as pd
import dotenv
from wikirate4py import API, Cursor
from warnings import warn
from wikirate4py.utils import to_dataframe


dotenv.load_dotenv(os.path.join(ROOT, ".env"))

wikirate = API(os.getenv("WIKIRATE_KEY"))


def filename_encode(metric_name: str, metric_designer: str):
    """Create valid filename from metric name and designer."""
    return (
        base64.urlsafe_b64encode(f"{metric_designer}+{metric_name}".encode("UTF-8"))
    ).decode("UTF-8")


def filename_decode(filename):
    """Decode metric name and designer from filename."""
    decoded = base64.urlsafe_b64decode(filename).decode("UTF-8").split("+")
    return {"metric_designer": decoded[0], "metric_name": decoded[1]}


async def download_metric(
    metric_name: str,
    metric_designer: str,
    task_id: int = -1,
    ignore_cache: bool = False,
):
    """Download metric from api."""
    # path management
    filename = filename_encode(metric_name=metric_name, metric_designer=metric_designer)
    outpath = os.path.join(DATADIR, "metrics", filename + ".csv")

    # check if file already exists
    # probably unneccessary, should be handled by download overview
    if os.path.exists(outpath) and not ignore_cache:
        warn(f"Using cached {metric_name} by {metric_designer}")
        return

    # scrape until cursor is empty
    cursor = Cursor(
        wikirate.get_answers,
        metric_name=metric_name,
        metric_designer=metric_designer,
        per_page=100,
    )
    answers = []
    while cursor.has_next():
        answers += cursor.next()

    df = to_dataframe(answers)
    df = df[["id", "metric", "company", "value", "year"]]
    # write to file
    df.to_csv(outpath, index=False)

    # return task id for bookkeeping, if download was successful
    return task_id


async def download_metrics(metrics_path: str = "", num_threads: int = 5):
    """Download all metrics listed in supplied file."""
    overview_path = os.path.join(DATADIR, "metric_download_overview.csv")

    # create overview file for storing timestamps
    if not os.path.exists(overview_path):
        overview = pd.read_csv(metrics_path)
        overview = overview[["ID", "Metric Title", "Metric Designer"]]
        overview["download_timestamp"] = np.nan
        overview.to_csv(overview_path, index=False)
    else:
        overview = pd.read_csv(overview_path)

    # create metric iterable with progress bar
    rows = overview.iterrows()
    progressbar = tqdm(desc="Downloading metrics", total=len(overview))

    # loop while unprocessed metric exists
    downloading = True
    while downloading:
        # batch job manager
        async with TaskGroup() as tg:
            tasks = []
            for _ in range(num_threads):
                try:
                    task_id, row = next(rows)
                except StopIteration:
                    downloading = False
                    break
                print(f"fetching {row['Metric Title']}")
                tasks.append(
                    tg.create_task(
                        download_metric(
                            task_id=task_id,
                            metric_name=row["Metric Title"],
                            metric_designer=row["Metric Designer"],
                        )
                    )
                )

            # wait until all tasks finished
            for task in tasks:
                task_id = await task
                progressbar.update()
                # if download happened, store timestamp
                if task_id:
                    overview.at[task_id, "download_timestamp"] = time()
            # persist after every batch
            overview.to_csv(overview_path, index=False)


if __name__ == "__main__":
    asyncio.run(download_metrics(CURATEDMETRICPATHS))
