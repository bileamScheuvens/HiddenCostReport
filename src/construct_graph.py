import os
from .constants import ROOT
from pyoxigraph import Store, NamedNode, Literal, Quad, Triple
from .data_sources.wikirate import parse_companies, parse_metrics, parse_scope1_emissions
import pyoxigraph as pox



def build_graph() -> Store:
    store = Store()

    with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
        store.load(f, pox.RdfFormat.TURTLE)

    company_id_lookup = parse_companies(store)
    parse_metrics(store)
    parse_scope1_emissions(store, company_id_lookup=company_id_lookup)
    return store, company_id_lookup
