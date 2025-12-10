import os
from time import time
from .constants import ROOT, GRAPHPATH
from pyoxigraph import Store
from .data_sources.wikirate import parse_companies, parse_metrics, parse_metric
from .harmonization import CompanyIDLookup
from .data_sources.openproductsfacts import parse_productsfacts
import pyoxigraph as pox



def build_graph(verbosity: int = 0) -> None:
    """Construct graph from all sources."""
    # init store
    store = Store(GRAPHPATH)
    store.clear()
    start = time()
    
    # load schema
    with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
        store.load(f, pox.RdfFormat.TURTLE)
    if verbosity:
        print(f"parsed schema after {time() - start}")

    store, company_id_lookup = parse_companies(store)
    company_id_lookup.save()
    if verbosity:
        print(f"parsed companies after {time() - start}")

    store = parse_metrics(store)
    if verbosity:
        print(f"parsed metric metadata after {time() - start}")

    store = parse_metric(store, metric_name="Revenue EUR", metric_designer="Clean Clothes Campaign", company_id_lookup=company_id_lookup)
    store = parse_metric(store, metric_name="Direct greenhouse gas (GHG) emissions (Scope 1), GRI 305-1-a (formerly G4-EN15-a)", metric_designer="Global Reporting Initiative", company_id_lookup=company_id_lookup)
    store = parse_metric(store, metric_name="Scope 3 Greenhouse Gas Emissions", metric_designer="GreenDex", company_id_lookup=company_id_lookup)
    if verbosity:
        print(f"parsed metrics after {time() - start}")
    parse_productsfacts(store)
    if verbosity:
        print(f"parsed openproductsfacts emissions after {time() - start}")
        print(f"total graph size: {len(store)}")


def load_graph() -> Store:
    store = Store(GRAPHPATH)
    return store

def load_idlookup() -> CompanyIDLookup:
    company_id_lookup = CompanyIDLookup()
    company_id_lookup.load()
    return company_id_lookup





