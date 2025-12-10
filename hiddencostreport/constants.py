import os

NS = "http://hiddencostreport.org/schema#"
ROOT = os.path.dirname(__file__)
DATADIR = os.path.join(os.path.expanduser("~"), "data", "hiddencostreport")

CURATEDMETRICPATHS = os.path.join(DATADIR, "metrics_curated.csv")
GRAPHPATH = os.path.join(DATADIR, "graph")
