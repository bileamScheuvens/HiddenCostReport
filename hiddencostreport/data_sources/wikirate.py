from wikirate4py import API, Cursor
from pyoxigraph import Store, NamedNode, Literal, Quad, BlankNode
from wikirate4py.models import Company
from wikirate4py.utils import to_dataframe
import dotenv
import pandas as pd
from pandas.core.series import Series
from typing import Tuple
import os
from warnings import warn
from .scrape_utils import filename_decode, filename_encode
from ..harmonization import CompanyIDLookup
from ..constants import ROOT, DATADIR, NS

dotenv.load_dotenv(os.path.join(ROOT, ".env"))

wikirate = API(os.getenv("WIKIRATE_KEY"))
# x = wikirate.get_metrics(identifier="Adidas AG")
# x = wikirate.get_answers(metric_name="Revenue EUR", metric_designer="Clean Clothes Campaign")
# print(x)


def download_metric(metric_name: str, metric_designer: str, ignore_cache: bool = False):
    # TODO async
    filename = filename_encode(metric_name=metric_name, metric_designer=metric_designer) 
    outpath = os.path.join(DATADIR, "metrics", filename+".csv")
    if os.path.exists(outpath) and not ignore_cache:
        warn(f"Using cached {metric_name} by {metric_designer}")
        return
    cursor = Cursor(wikirate.get_answers, metric_name=metric_name, metric_designer=metric_designer)
    answers = []
    while cursor.has_next():
        answers += cursor.next()

    df = to_dataframe(answers)
    df = df[["id", "metric", "company", "value", "year"]]
    df.to_csv(outpath, index=False)




def parse_metrics(store: Store, filename: str = "metrics_500.csv"):
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



def parse_scope1_emissions(store: Store, filename: str = "scope1_emissions.csv", company_id_lookup: dict = {}):
    def _parse_row(x: Series):
        if x["Company"] not in company_id_lookup:
            return
        observation = BlankNode()
        company = NamedNode(company_id_lookup[x["Company"]])
        # TODO: link to actual metric
        store.add(Quad(company, NamedNode(NS+"hasMetric"), observation))
        store.add(Quad(observation, NamedNode(NS+"MetricName"), Literal(x["Metric"])))
        store.add(Quad(observation, NamedNode(NS+"Year"), Literal(x["Year"])))
        store.add(Quad(observation, NamedNode(NS+"Value"), Literal(x["Value"])))

    emissions = pd.read_csv(os.path.join(DATADIR, "metrics", filename))
    emissions.apply(_parse_row, axis=1)

def parse_metric(store: Store, metric_name: str, metric_designer:str, company_id_lookup: dict = {}):
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


# download_metric(metric_name="Revenue EUR", metric_designer="Clean Clothes Campaign")
download_metric(metric_name="Revenue EUR", metric_designer="Clean Clothes Campaign")
download_metric(metric_name="Direct greenhouse gas (GHG) emissions (Scope 1), GRI 305-1-a (formerly G4-EN15-a)", metric_designer="Global Reporting Initiative")
download_metric(metric_name="Scope 3 Greenhouse Gas Emissions", metric_designer="GreenDex")
