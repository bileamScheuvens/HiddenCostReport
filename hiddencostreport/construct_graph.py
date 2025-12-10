import os
import pandas as pd
from time import time
from tqdm import tqdm
from .constants import ROOT, CURATEDMETRICPATHS
from .data_sources.wikirate import parse_companies, parse_metrics, parse_metric
from .harmonization import GraphManager
from .data_sources.openproductsfacts import parse_productsfacts
import pyoxigraph as pox



def construct_graph(verbosity: int = 0, metrics_path: str = CURATEDMETRICPATHS) -> None:
    """Construct graph from all sources."""
    # init store
    graph = GraphManager()
    graph.clear()
    start = time()
    
    # load schema
    with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
        graph.load(f, pox.RdfFormat.TURTLE)
    if verbosity:
        print(f"parsed schema after {time() - start}")

    parse_companies(graph)
    graph.save()
    if verbosity:
        print(f"parsed companies after {time() - start}")

    parse_metrics(graph)
    graph.save()
    if verbosity:
        print(f"parsed metric metadata after {time() - start}")

     

    metrics = pd.read_csv(metrics_path)
    tqdm.pandas()
    metrics.progress_apply(lambda row: parse_metric(graph, metric_designer=row["Metric Designer"], metric_name=row["Metric Title"]), axis=1)
    
    if verbosity:
        print(f"parsed metrics after {time() - start}")
    parse_productsfacts(graph)
    if verbosity:
        print(f"parsed openproductsfacts emissions after {time() - start}")
        print(f"total graph size: {len(graph)}")






