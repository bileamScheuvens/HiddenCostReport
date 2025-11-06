import os
from constants import ROOT
from pyoxigraph import Store, NamedNode, Literal, Triple
import pyoxigraph as pox

store = Store()
ns = ":"


with open(os.path.join(ROOT, "..", "graph", "schema.ttl")) as f:
    store.add_graph(pox.parse(input=f, format=pox.RdfFormat.TURTLE))

company = NamedNode(ns + "HandM")
store.add(Triple(company, NamedNode(ns+"WikirateID"), "Q188326"))

emissions_scope1 = NamedNode(ns + "emissions_scope1_HandM")
store.add(Triple(company, NamedNode(ns+"hasMetric"), emissions_scope1))
store.add(Triple(emissions_scope1, NamedNode("http://schema.org/name"), Literal("emissions_scope1")))
store.add(Triple(emissions_scope1, NamedNode("http://schema.org/value"), Literal(16.354)))
store.add(Triple(emissions_scope1, NamedNode("http://schema.org/unit"), Literal("tonnes")))
