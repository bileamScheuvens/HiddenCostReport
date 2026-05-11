import os

NS = "http://hiddencostreport.org/schema#"
ROOT = os.path.dirname(__file__)
DATADIR = os.path.join(os.path.expanduser("~"), "data", "hiddencostreport")

CURATEDMETRICPATHS = os.path.join(DATADIR, "metrics_curated.csv")
METRICSPATH = os.path.join(DATADIR, "metrics_1000.csv")
COMPANIESPATH = os.path.join(DATADIR, "companies_1000.csv")
GRAPHPATH = os.path.join(DATADIR, "graph")
QLEVERDIR = os.path.join(ROOT, "..", "qlever")
DIAGRAMDIR = os.path.join(ROOT, "..", "report", "res")
