from wikirate4py import API
from pyoxigraph import Store, NamedNode, Literal, Quad, BlankNode
from wikirate4py.models import Company
import dotenv
import pandas as pd
from pandas.core.series import Series
import os
from ..constants import ROOT, DATADIR, NS

dotenv.load_dotenv(os.path.join(ROOT, ".env"))

# wikirate = API(os.getenv("WIKIRATE_KEY"))
# x = wikirate.get_metrics(identifier="H & M")
# print(x)



def parse_metrics(store: Store, filename: str = "metrics_500.csv"):
    def _parse_metric_row(x: Series):
        # construct name with prefix M for metric
        metric = NamedNode(NS + "M" + x["ID"][1:])
        store.add(Quad(metric, NamedNode(NS+"Title"), Literal(x["Metric Title"])))
        store.add(Quad(metric, NamedNode(NS+"Designer"), Literal(x["Metric Designer"])))
        store.add(Quad(metric, NamedNode(NS+"Questions"), Literal(x["Questions"])))
        store.add(Quad(metric, NamedNode(NS+"ValueType"), Literal(x["Value Type"])))
        store.add(Quad(metric, NamedNode(NS+"Unit"), Literal(x["Unit"])))

    metrics = pd.read_csv(os.path.join(DATADIR, filename))
    metrics.apply(_parse_metric_row, axis=1)



def parse_companies(store: Store, filename: str = "companies_100.csv") -> dict:
    """Parse companies from csv to rdf and return lookup for id. """
    company_id_lookup = {}
    def _parse_company_row(x: Series):
        # construct name with prefix C for company
        id = NS + "C" + str(x["ID"])
        company = NamedNode(id)
        company_id_lookup[x["Name"]] = id

        store.add(Quad(company, NamedNode(NS+"Name"), Literal(x["Name"])))

        if not pd.isna(x["OpenCorporates ID"]):
            store.add(Quad(company, NamedNode(NS+"OpenCorporatesID"), Literal(x["OpenCorporates ID"])))

    companies = pd.read_csv(os.path.join(DATADIR, filename))
    companies.apply(_parse_company_row, axis=1)
    return company_id_lookup



def parse_scope1_emissions(store: Store, filename: str = "scope1_emissions.csv", company_id_lookup = {}):
    def _parse_row(x: Series):
        if x["Company"] not in company_id_lookup:
            return
        observation = BlankNode()
        company = NamedNode(company_id_lookup[x["Company"]])
        store.add(Quad(company, NamedNode(NS+"hasMetric"), observation))
        store.add(Quad(observation, NamedNode(NS+"MetricName"), Literal(x["Metric"])))
        store.add(Quad(observation, NamedNode(NS+"Year"), Literal(x["Year"])))
        store.add(Quad(observation, NamedNode(NS+"Value"), Literal(x["Value"])))

    emissions = pd.read_csv(os.path.join(DATADIR, "metrics", filename))
    emissions.apply(_parse_row, axis=1)


