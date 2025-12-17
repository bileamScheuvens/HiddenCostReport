from pyoxigraph import NamedNode, Literal, Quad, BlankNode
import pandas as pd
from pandas.core.series import Series
import os
import networkx as nx
from tqdm import tqdm
from .scrape_utils import filename_encode
from ..constants import DATADIR, NS, CURATEDMETRICPATHS
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph_manager import GraphManager


def parse_metrics_metadata(graph: "GraphManager", filename: str = "metrics_500.csv"):
    """Parse metrics csv into rdf."""
    def _parse_metric_row(x: Series):
        # construct name with prefix M for metric
        id = NS + "M" + x["ID"][1:]
        metric = NamedNode(id)
        graph.set_metric_id(metric_designer=x["Metric Designer"], metric_name=x["Metric Title"], id=id)

        graph.add(Quad(metric, NamedNode(NS+"MetricDesigner"), Literal(x["Metric Designer"])))
        graph.add(Quad(metric, NamedNode(NS+"MetricTitle"), Literal(x["Metric Title"])))
        graph.add(Quad(metric, NamedNode(NS+"Questions"), Literal(x["Questions"])))
        graph.add(Quad(metric, NamedNode(NS+"ValueType"), Literal(x["Value Type"])))
        graph.add(Quad(metric, NamedNode(NS+"Unit"), Literal(x["Unit"])))

    metrics = pd.read_csv(os.path.join(DATADIR, filename))
    metrics.apply(_parse_metric_row, axis=1)

def example_metrics_metadata() -> nx.DiGraph:
    edges = {
        "MetricDesigner": "<Metric Designer>",
        "MetricTitle": "<Metric Title>",
        "Question": "<Question>",
        "Value Type": "<Value Type>",
        "Unit": "<Unit>",
    }
    
    G = nx.DiGraph()
    center = "M<xxxxx>"
    G.add_node(center)
    for (p,o) in edges.items():
        G.add_edge(center, o, label=p)
    return G



def parse_companies(graph: "GraphManager", filename: str = "companies_100.csv") -> None:
    """Parse companies from csv to rdf and return lookup for id. """
    def _parse_company_row(x: Series):
        # construct name with prefix C for company
        id = NS + "C" + str(x["ID"])
        company = NamedNode(id)
        graph.set_company_id(x["Name"], id)
        # TODO: Columnms are misaligned, aliases are in headquarters. Fix
        aliases = x["Headquarters"]
        if not pd.isna(aliases):
            for alias in aliases.split(";"):
                graph.set_company_id(alias, id)
                

        graph.add(Quad(company, NamedNode(NS+"Name"), Literal(x["Name"])))

        if not pd.isna(x["OpenCorporates ID"]):
            graph.add(Quad(company, NamedNode(NS+"OpenCorporatesID"), Literal(x["OpenCorporates ID"])))

    companies = pd.read_csv(os.path.join(DATADIR, filename))
    companies.apply(_parse_company_row, axis=1)


def example_companies() -> nx.DiGraph:
    edges = {
        "Name": "<Name>",
        "OpenCorporatesID": "<OpenCorporates ID>",
    }
    
    G = nx.DiGraph()
    center = "C<xxxxx>"
    G.add_node(center)
    for (p,o) in edges.items():
        G.add_edge(center, o, label=p)
    return G


def parse_metric(graph: "GraphManager", metric_name: str, metric_designer:str) -> None:
    """Parse individual metric into rdf."""
    def _parse_row(x: Series):
        if x["company"] not in graph.company_id_lookup:
            return
        observation = BlankNode()
        company = NamedNode(graph.get_company_id(x["company"]))
        graph.add(Quad(company, NamedNode(NS+"hasMetric"), observation))
        graph.add(Quad(observation, NamedNode(NS+"MetricID"), NamedNode(graph.metric_id_lookup[x["metric"]])))
        graph.add(Quad(observation, NamedNode(NS+"Year"), Literal(x["year"])))
        graph.add(Quad(observation, NamedNode(NS+"Value"), Literal(x["value"])))

    filename = filename_encode(metric_name=metric_name, metric_designer=metric_designer)
    df = pd.read_csv(os.path.join(DATADIR, "metrics", filename+".csv"))
    df.apply(_parse_row, axis=1)

def example_metric() -> nx.DiGraph:
    edges = {
        "MetricID": "M<xxxx>",
        "Year": "<Year>",
        "Value": "<Value>",
    }
    
    G = nx.DiGraph()
    center = "BLANK"
    G.add_node(center)
    for (p,o) in edges.items():
        G.add_edge(center, o, label=p)
    G.add_edge("C<xxxx>", center, label="hasMetric")
    return G

def parse_metrics(graph: "GraphManager", metrics_path: str = CURATEDMETRICPATHS) -> None:
    metrics = pd.read_csv(metrics_path)
    tqdm.pandas()
    metrics.progress_apply(lambda row: parse_metric(graph, metric_designer=row["Metric Designer"], metric_name=row["Metric Title"]), axis=1)
