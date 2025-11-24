import os
from time import time
from .constants import ROOT, DATADIR
from pyoxigraph import Store, NamedNode, Literal, Quad, Triple
from .data_sources.wikirate import parse_companies, parse_metrics, parse_scope1_emissions
from .data_sources.openproductsfacts import parse_productsfacts
import pyoxigraph as pox




def build_graph() -> Store:
    store = Store(os.path.join(DATADIR, "graph"))
    start = time()
    
    with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
        store.load(f, pox.RdfFormat.TURTLE)
    print(f"parsed schema after {time() - start}")

    company_id_lookup = parse_companies(store)
    print(f"parsed companies after {time() - start}")
    parse_metrics(store)
    print(f"parsed metrics after {time() - start}")

    parse_scope1_emissions(store, company_id_lookup=company_id_lookup)
    print(f"parsed scope1 emissions after {time() - start}")
    parse_productsfacts(store)
    print(f"parsed openproductsfacts emissions after {time() - start}")
    return store, company_id_lookup

build_graph()
