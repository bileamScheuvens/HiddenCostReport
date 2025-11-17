from wikirate4py import API
from pyoxigraph import Store, NamedNode, Literal, Quad
from wikirate4py.models import Company
import dotenv
import pandas as pd
from pandas.core.series import Series
import os
from ..constants import ROOT, DATADIR

dotenv.load_dotenv(os.path.join(ROOT, ".env"))

# wikirate = API(os.getenv("WIKIRATE_KEY"))
# x = wikirate.get_metrics(identifier="H & M")
# print(x)



ns = "http://hiddencostreport.org/schema#"

def parse_metrics(store: Store, filename: str = "metrics_500.csv"):
    def _parse_metric_row(x: Series):
        # construct name with prefix M for metric
        metric = NamedNode(ns + "M" + x["ID"][1:])
        store.add(Quad(metric, NamedNode(ns+"Title"), Literal(x["Metric Title"])))
        store.add(Quad(metric, NamedNode(ns+"Designer"), Literal(x["Metric Designer"])))
        store.add(Quad(metric, NamedNode(ns+"Questions"), Literal(x["Questions"])))
        store.add(Quad(metric, NamedNode(ns+"ValueType"), Literal(x["Value Type"])))
        store.add(Quad(metric, NamedNode(ns+"Unit"), Literal(x["Unit"])))

    metrics = pd.read_csv(os.path.join(DATADIR, filename))
    metrics.apply(_parse_metric_row, axis=1)



def parse_companies(store: Store, filename: str = "companies_100.csv"):
    def _parse_company_row(x: Series):
        # construct name with prefix C for company
        company = NamedNode(ns + "C" + str(x["ID"]))

        store.add(Quad(company, NamedNode(ns+"Name"), Literal(x["Name"])))
        if x["OpenCorporates ID"]:
            store.add(Quad(company, NamedNode(ns+"OpenCorporatesID"), Literal(x["OpenCorporates ID"])))

    companies = pd.read_csv(os.path.join(DATADIR, filename))
    companies.apply(_parse_company_row, axis=1)



# TODO: figure out how to extract company reliably
# def parse_scope1_emissions(store: Store, filename: str = "scope1_emissions.csv", wikirateID: str = "M19822855"):
#     def _parse_row(x: Series):
#
#
#     emissions = pd.read_csv(os.path.join(DATADIR, filename))


