import asyncio
import base64
import os
from asyncio import TaskGroup

from time import time, sleep
from warnings import warn


import dotenv
import numpy as np
import pandas as pd
from tqdm import tqdm
from wikirate4py import API, Cursor
from wikirate4py.utils import to_dataframe
from wikirate4py.exceptions import WikirateServerErrorException

from ..constants import CURATEDMETRICPATHS, DATADIR, METRICSPATH, ROOT

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
    try:
        while cursor.has_next():
            answers += cursor.next()
            # throttle download
            sleep(1)
    # except WikirateServerErrorException:
    except Exception as e:
        warn(
            f"Error for {metric_name}+{metric_designer}, skipping. {e}.\nDiscarding {len(answers)} elements."
        )
        return

    df = to_dataframe(answers)
    try:
        df = df[["id", "metric", "company", "value", "year"]]
        # write to file
        df.to_csv(outpath, index=False)
    except Exception as e:
        warn(
            f"Error for {metric_name}+{metric_designer}, skipping. {e}.\nDiscarding {len(answers)} elements."
        )
        return

    # return task id for bookkeeping, if download was successful
    return task_id


async def download_metrics(
    metrics_path: CURATEDMETRICPATHS, num_threads: int = 5, ignore_cache: bool = False
):
    """Download all metrics listed in supplied file."""
    overview_path = os.path.join(DATADIR, "metric_download_overview.csv")

    # create overview file for storing timestamps
    if not os.path.exists(overview_path) or ignore_cache:
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
    asyncio.run(download_metrics(METRICSPATH))
