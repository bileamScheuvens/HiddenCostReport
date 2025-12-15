import os
from .constants import GRAPHPATH
from pyoxigraph import Store
import pandas as pd
from time import time
from tqdm import tqdm
from .constants import ROOT, CURATEDMETRICPATHS
from .data_sources.wikirate import parse_companies, parse_metrics, parse_metric
from .harmonization import CompanyIDLookup, MetricIDLookup
from .data_sources.openproductsfacts import parse_productsfacts
import pyoxigraph as pox


class GraphManager():
    """Wrapper around graph store, which handles harmonized access and lookup tables."""

    def __init__(self, *args, **kwargs):
        self.store = Store(GRAPHPATH)
        self.company_id_lookup = CompanyIDLookup()
        self.company_id_lookup.load()
        self.metric_id_lookup = MetricIDLookup()
        self.metric_id_lookup.load()

    def add(self, *args, **kwargs):
        self.store.add(*args, **kwargs)

    def load(self, *args, **kwargs):
        self.store.load(*args, **kwargs)

    def query(self, *args, **kwargs):
        return self.store.query(*args, **kwargs)

    def clear(self):
        self.store.clear()

    def __len__(self):
        return len(self.store)

    def graph_summary(self):
        return {
                "Triples": len(self),
                "Companies": len(self.company_id_lookup),
                "Metrics": len(self.metric_id_lookup),
                }


    def autocomplete_search(self, search_type: str, term: str):
        if search_type == "company":
            return self.company_id_lookup.autocomplete_search(term)
        elif search_type == "metric":
            return self.metric_id_lookup.autocomplete_search(term)
        else:
            raise NotImplementedError()

    def get_metric_id(self, metric_designer: str, metric_name: str) -> str:
        return self.metric_id_lookup[f"{metric_designer}+{metric_name}"]

    def set_metric_id(self, metric_designer: str, metric_name: str, id: str) -> None:
        self.metric_id_lookup[f"{metric_designer}+{metric_name}"] = id
    
    def get_company_id(self, company_name: str) -> str:
        return self.company_id_lookup[company_name]

    def set_company_id(self, company_name: str, id: str) -> None:
        self.company_id_lookup[company_name] = id

    def save(self):
        self.company_id_lookup.save()
        self.metric_id_lookup.save()

    def rebuild_graph(self, verbosity: int = 1, metrics_path: str = CURATEDMETRICPATHS) -> None:
        """Construct graph from all sources."""
        # TODO: pass store to parse funcs directly instead of graphmanager
        # init store
        self.store.clear()
        start = time()
        
        # load schema
        with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
            self.load(f, pox.RdfFormat.TURTLE)
        if verbosity:
            print(f"parsed schema after {time() - start}")

        parse_companies(self)
        self.save()
        if verbosity:
            print(f"parsed companies after {time() - start}")

        parse_metrics(self)
        self.save()
        if verbosity:
            print(f"parsed metric metadata after {time() - start}")

         

        metrics = pd.read_csv(metrics_path)
        tqdm.pandas()
        metrics.progress_apply(lambda row: parse_metric(self, metric_designer=row["Metric Designer"], metric_name=row["Metric Title"]), axis=1)
        
        if verbosity:
            print(f"parsed metrics after {time() - start}")
        parse_productsfacts(self)
        if verbosity:
            print(f"parsed openproductsfacts emissions after {time() - start}")
            print(f"total graph size: {len(self)}")







