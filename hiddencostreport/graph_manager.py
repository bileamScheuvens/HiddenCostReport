import os
from .constants import GRAPHPATH
import pandas as pd
from pyoxigraph import Store

from time import time
from .constants import ROOT, METRICSPATH, QLEVERDIR
from .data_sources import SOURCES
from .harmonization import CompanyIDLookup, MetricIDLookup
import pyoxigraph as pox


class GraphManager:
    """Wrapper around graph store, which handles harmonized access and lookup tables."""

    def __init__(self, *args, **kwargs):
        self.store = Store(GRAPHPATH)
        self.company_id_lookup = CompanyIDLookup()
        self.company_id_lookup.load()
        self.metric_id_lookup = MetricIDLookup()
        self.metric_id_lookup.load()

    def add(self, *args, **kwargs):
        """Passthrough to store."""
        self.store.add(*args, **kwargs)

    def load(self, *args, **kwargs):
        """Passthrough to store."""
        self.store.load(*args, **kwargs)

    def query(self, *args, **kwargs):
        """Run query and return as Dataframe."""
        query_result = self.store.query(*args, **kwargs)
        df = []
        for row in query_result:
            try:
                df.append(list(map(lambda x: x.value, row)))
            except:
                pass

        df = pd.DataFrame(df)
        if not df.empty:
            df.columns = list(map(str, query_result.variables))
        return df

    def clear(self):
        """Passthrough to store."""
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

    def serialize(self):
        with open(os.path.join(QLEVERDIR, "serialized.ttl"), "wb") as f:
            self.store.dump(f, pox.RdfFormat.TURTLE, from_graph=pox.DefaultGraph())

    def rebuild_graph(
        self, verbosity: int = 1, metrics_path: str = METRICSPATH
    ) -> None:
        """Construct graph from all sources."""
        # init store
        self.store.clear()
        start = time()

        # load schema
        with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
            self.store.load(f, pox.RdfFormat.TURTLE)
        if verbosity:
            print(f"parsed schema after {time() - start}")

        for source in SOURCES:
            if not source.active:
                continue
            source.parse(graph=self)
            if verbosity:
                print(f"parsed {source.name} after {time() - start} secs")

        self.save()
        if verbosity:
            print(f"total graph size: {len(self)}")
