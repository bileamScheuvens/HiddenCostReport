import os
from constants import ROOT
from pyoxigraph import Store, NamedNode, Literal, Quad, Triple
import pyoxigraph as pox

store = Store()
ns = "http://hiddencostreport.org/schema#"
ns_sources = "http://hiddencostreport.org/sources/"




with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
    store.load(f, pox.RdfFormat.TURTLE)

company = NamedNode(ns + "H&M")
store.add(Quad(company, NamedNode(ns+"WikirateID"), Literal("Q188326")))

emission1_graph = NamedNode(ns_sources + "emissions_scope1")
emissions_scope1 = NamedNode(ns + "emissions_scope1_HandM")
store.add(Quad(company, NamedNode(ns+"hasMetric"), emissions_scope1))
store.add(Quad(emissions_scope1, NamedNode("http://schema.org/name"), Literal("emissions_scope1")))
store.add(Quad(emissions_scope1, NamedNode("http://schema.org/value"), Literal(16.354)))
store.add(Quad(emissions_scope1, NamedNode("http://schema.org/unit"), Literal("tonnes")))



# run basic query
query = f"""
SELECT ?s ?o WHERE {{
?s <{ns}WikirateID> ?o .
}}
"""
for row in store.query(query):
    print(row['s'])
