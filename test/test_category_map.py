from hiddencostreport.harmonization import CategoryMapper
from hiddencostreport.constants import DATADIR
import pandas as pd
import os
import pytest


def test_metric_coverage(request):
    """Test metric coverage by mapping all metrics to their category and printing distribution."""
    df = pd.read_csv(os.path.join(DATADIR, "metrics_1000.csv"))
    df["category"] = df.apply(
        lambda row: CategoryMapper().assign_category(
            metric_designer=row["Metric Designer"],
            metric_title=row["Metric Title"],
            questions=row["Questions"],
            value_type=row["Value Type"],
        ),
        axis=1,
    )
    df.sort_values(by="category", inplace=True)
    df[["ID", "category", "Metric Title", "Value Type", "Questions"]].to_csv(
        os.path.join(DATADIR, "test_artifacts", "mapped.csv"), index=False
    )
    grouped = df.groupby("category")["ID"].count()

    request.config.metric_coverage = str(grouped)
    # TODO: set threshhold for unmapped?
