#import "@preview/abbr:0.3.0"
#show: abbr.show-rule
#abbr.make(
  ("TCA", "True Cost Accounting"),
  ("ESG", "Environmental Social and Governance"),
  ("NGO", "Non Government Organization"),
  ("ATCA", "Approximate True Cost Accounting"),
  ("RDF", "Resource Description Framework"),
  ("SPARQL", "SPARQL Protocol and RDF Query Language"),
)

#set document(title: [Open Data Fusion for Approximate True Cost Accounting using Knowledge Graphs])

#set heading(numbering: "1.")

#align(center)[
  #title()
]


#pagebreak()

#outline()

#pagebreak()


// = Abstract
//
// = Introduction
//
// - explain why economics fails
// - explain rdf+sparql
//
//
// = Related Work
// - teebagrifood
// - true price method
//
// = Methodology
// - graph construction
//   - sources
//   - harmonization
//     - manual cleanup
//   - categorization
// - graph utilization
//   - qlever
//   - ui
//   - query translation
//
//
// = Evaluation
// - comparison to trueprice reports
// - graph itself (wang21)
// - query translation
//
// = Discussion
// - usefulness
// - shortcomings
// - future work
//   - product level
//   - text integration
//   - better pricing
//   - better category mapping

= Abstract

= Introduction

= Related Work

= Methodology
At the core of this work lies the knowledge graph, which the platform surrounding it attempts to make easily more accessible.
This section is therefore divided into graph construction (including maintenance) and graph utilization.

== Graph Construction
The data ingestion phase is designed to be flexible and extensible to serve different use cases.
Inclusion of sources can be toggled in the interface. With the currently available sources graph construction and indexing takes arounda minute on consumer hardware. This is subject to change with the inclusion of more or remote sources.
After adding the schema (see @appendix_schema[Appendix]), each source is parsed into triples and stored using the graph database oxigraph (CITATION)


The availabe sources are described in the following.

=== Source: Wikirate
Wikirate @Wikirate is an open data platform, which crowdsources and hosts a variety of company data relating to @ESG issues.
Each data point regardless of type (Company, Metric, Project, Tag, Image, ...) lives in a shared namespace as so called cards, which can be fetched from an API.\
To include wikirate in the graph, a subset#footnote[This selection is done purely for scoping reasons. The data has a long tail of largely isolated and therefore less interesting elements.] of 1000 companies with most data points associated is selected, alongside the 1000 most bookmarked metrics.
These are cached and transformed from tabular format into triples, conforming to the schema described in @appendix_schema[Appendix].


=== Source: Openproductfacts




= Graph Utilization



= Evaluation

= Discussion

= Appendix

== Graph Schema <appendix_schema>

```ttl
@prefix : <http://hiddencostreport.org/schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .

@prefix wr: <https://wikirate.org> .


:Company a rdfs:Class .
:Product a rdfs:Class .
:Article a rdfs:Class .
:Metric a rdfs:Class .
:Observation a rdfs:Class .
:Dataset a rdfs:Class .
:Datapoint a rdfs:Class .
:Product a rdfs:Class .

:Name a rdf:property ;
  rdfs:range rdfs:literal .

:OpenCorporatesID a rdf:property ;
  rdfs:domain :Company ;
  rdfs:range rdfs:literal .

:MetricTitle a rdf:property ;
  rdfs:domain :Metric ;
  rdfs:range rdfs:literal .

:MetricDesigner a rdf:property ;
  rdfs:domain :Metric ;
  rdfs:range rdfs:literal .

:Questions a rdf:property ;
  rdfs:domain :Metric ;
  rdfs:range rdfs:literal .

:ValueType a rdf:property ;
  rdfs:domain :Metric ;
  rdfs:range rdfs:literal .

:Unit a rdf:property ;
  rdfs:domain :Metric ;
  rdfs:range rdfs:literal .

:hasMetric a rdf:property;
  rdfs:domain :Company ;
  rdfs:range :Observation .

:Brand a rdf:property ;
  rdfs:domain :Product .

:Ingredient a rdf:property ;
  rdfs:domain :Product .

:ManufacturedIn a rdf:property ;
  rdfs:domain :Product .


```

#bibliography("hiddencostreport.bib")



