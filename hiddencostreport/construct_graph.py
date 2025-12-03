import os
from time import time
from typing import Tuple 
from .constants import ROOT, DATADIR
from pyoxigraph import Store
from .data_sources.wikirate import parse_companies, parse_metrics, parse_scope1_emissions, parse_metric
from .harmonization import CompanyIDLookup
from .data_sources.openproductsfacts import parse_productsfacts
import pyoxigraph as pox




def build_graph() -> Tuple[Store, CompanyIDLookup]:
    store = Store(os.path.join(DATADIR, "graph"))
    store.clear()
    start = time()
    
    with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
        store.load(f, pox.RdfFormat.TURTLE)
    print(f"parsed schema after {time() - start}")

    store, company_id_lookup = parse_companies(store)
    print(f"parsed companies after {time() - start}")
    store = parse_metrics(store)
    print(f"parsed metrics after {time() - start}")

    store = parse_metric(store, metric_name="Revenue EUR", metric_designer="Clean Clothes Campaign", company_id_lookup=company_id_lookup)
    print(len(store))
    store = parse_metric(store, metric_name="Direct greenhouse gas (GHG) emissions (Scope 1), GRI 305-1-a (formerly G4-EN15-a)", metric_designer="Global Reporting Initiative")
    print(len(store))
    store = parse_metric(store, metric_name="Scope 3 Greenhouse Gas Emissions", metric_designer="GreenDex")
    print(f"parsed concrete metrics after {time() - start}")
    # parse_scope1_emissions(store, company_id_lookup=company_id_lookup)
    # print(f"parsed scope1 emissions after {time() - start}")
    # parse_productsfacts(store)
    # print(f"parsed openproductsfacts emissions after {time() - start}")
    return store, company_id_lookup


