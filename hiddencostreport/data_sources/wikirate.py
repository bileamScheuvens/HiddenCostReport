from pyoxigraph import Store, NamedNode, Literal, Quad, BlankNode
import pandas as pd
from pandas.core.series import Series
from typing import Tuple
import os
from .scrape_utils import filename_encode
from ..harmonization import CompanyIDLookup
from ..constants import DATADIR, NS


def parse_metrics(store: Store, filename: str = "metrics_500.csv"):
    """Parse metrics csv into rdf."""
    def _parse_metric_row(x: Series):
        # construct name with prefix M for metric
        metric = NamedNode(NS + "M" + x["ID"][1:])
        store.add(Quad(metric, NamedNode(NS+"MetricTitle"), Literal(x["Metric Title"])))
        store.add(Quad(metric, NamedNode(NS+"MetricDesigner"), Literal(x["Metric Designer"])))
        store.add(Quad(metric, NamedNode(NS+"Questions"), Literal(x["Questions"])))
        store.add(Quad(metric, NamedNode(NS+"ValueType"), Literal(x["Value Type"])))
        store.add(Quad(metric, NamedNode(NS+"Unit"), Literal(x["Unit"])))

    metrics = pd.read_csv(os.path.join(DATADIR, filename))
    metrics.apply(_parse_metric_row, axis=1)
    return store



def parse_companies(store: Store, filename: str = "companies_100.csv") -> Tuple[Store, CompanyIDLookup]:
    """Parse companies from csv to rdf and return lookup for id. """
    company_id_lookup = CompanyIDLookup()
    def _parse_company_row(x: Series):
        # construct name with prefix C for company
        id = NS + "C" + str(x["ID"])
        company = NamedNode(id)
        company_id_lookup[x["Name"]] = id
        # TODO: Columnms are misaligned, aliases are in headquarters. Fix
        aliases = x["Headquarters"]
        if not pd.isna(aliases):
            for alias in aliases.split(";"):
                company_id_lookup[alias] = id
                

        store.add(Quad(company, NamedNode(NS+"Name"), Literal(x["Name"])))

        if not pd.isna(x["OpenCorporates ID"]):
            store.add(Quad(company, NamedNode(NS+"OpenCorporatesID"), Literal(x["OpenCorporates ID"])))

    companies = pd.read_csv(os.path.join(DATADIR, filename))
    companies.apply(_parse_company_row, axis=1)
    return store, company_id_lookup



def parse_metric(store: Store, metric_name: str, metric_designer:str, company_id_lookup: dict = {}):
    """Parse individual metric into rdf."""
    def _parse_row(x: Series):
        if x["company"] not in company_id_lookup:
            return
        observation = BlankNode()
        company = NamedNode(company_id_lookup[x["company"]])
        # TODO: link to actual metric
        store.add(Quad(company, NamedNode(NS+"hasMetric"), observation))
        store.add(Quad(observation, NamedNode(NS+"MetricName"), Literal(x["metric"])))
        store.add(Quad(observation, NamedNode(NS+"Year"), Literal(x["year"])))
        store.add(Quad(observation, NamedNode(NS+"Value"), Literal(x["value"])))

    filename = filename_encode(metric_name=metric_name, metric_designer=metric_designer)
    df = pd.read_csv(os.path.join(DATADIR, "metrics", filename+".csv"))
    df.apply(_parse_row, axis=1)
    return store

