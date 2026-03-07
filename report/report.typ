#import "@preview/abbr:0.3.0"
#show: abbr.show-rule
#abbr.make(
  ("TCA", "True Cost Accounting"),
  ("ESG", "Environmental Social and Governance"),
  ("LLM", "Large Language Model"),
  ("KG", "Knowledge Graphs"),
  ("NGO", "Non Government Organization"),
  ("ATCA", "Approximate True Cost Accounting"),
  ("RDF", "Resource Description Framework"),
  ("SPARQL", "SPARQL Protocol and RDF Query Language"),
  ("SDG", "Sustainable Development Goals"),
)

#set document(title: [Open Data Fusion for Approximate True Cost Accounting using Knowledge Graphs])

#set heading(numbering: "1.")

#align(center)[
  #title()
  #v(20%)
  *Abstract*
]




#pagebreak()

#outline()

#pagebreak()


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


= Introduction
Neglecting costs which affect third parties in economic transactions leads to false equilibria in price finding.
This not only reduces market efficiency but incentivizes unsustainable behavior and exaggerates wealth concentration, since society eseentially pays for subsidies of individual actors.

To counteract this, one would have to consider (and assign costs to) all externalities relevant for the production of a good.
This difficult and time consuming practice is called @TCA.




// - explain why economics fails
// - explain rdf+sparql
// - explain price gap

= Related Work

= Methodology
At the core of this work lies the @KG, which the platform surrounding it attempts to make easily more accessible.
This section is therefore divided into graph construction (including maintenance) and graph utilization.


== Graph Construction
The data ingestion phase is designed to be flexible and extensible to serve different use cases.
Inclusion of sources can be toggled in the interface. With the currently available sources graph construction and indexing is a matter of minutes on consumer hardware. This is subject to change with the inclusion of more or remote sources.
After adding the schema (see @appendix_schema), each source is parsed into triples and stored using the graph database oxigraph @pellissiertanonOxigraph2026.

The availabe sources are described in the following.

=== Source: Wikirate
Wikirate @Wikirate is an open data platform, which crowdsources and hosts a variety of company data relating to @ESG issues.
Each data point regardless of type (Company, Metric, Project, Tag, Image, ...) lives in a shared namespace as so called cards, which can be fetched from an API.\
To include wikirate in the graph, a subset#footnote[This selection is done purely for scoping reasons. The source has a long tail of largely isolated and therefore less interesting data points.] of 1000 companies with most data points associated is selected, alongside the 1000 most bookmarked metrics.
These are cached and transformed from tabular format into triples, conforming to the schema described in @appendix_schema.


=== Source: OpenFoodFacts & OpenProductsFacts




= Graph Utilization


= Evaluation
Evaluation of the system can be approached from several directions.
One can measure the initial target of approximating true cost, by comparing output to existing true cost report.
Secondly one can examine the graph on its own and apply traditional @KG quality measures.
Lastly one can qualitative judge the performance of the @LLM query translation component.


== True Cost Accuracy
Many existing @TCA reports (@environmentTEEBAgriFoodEvaluationFramework2024 @michalkeTrueCostAccounting2023a @truepricefood, @truepriceapple, @truepricejeans) focus on a single product. Unfortunately the lack of data granularity makes this difficult to reproduce.
As a rough approximation we compute the hidden costs per dollar of revenue for a company and multiply this with the price of a product to get the hidden cost.
This approach has several assumptions which do not hold in practice:
- All products contribute to all metrics in proportion to their price.
- The entire supply chain is operated by the same company #footnote[There are inconsistencies between metrics, scope 2 and 3 emissions for example, account for external factors, while water usage only accounts for in house consumption.]
- The costs associated with metrics are location independent.

To approximate @truepricejeans, we may examine a denim Brand such as Levi Strauss and compute the price gap from the available metrics.
// TODO

== @KG Assessment
@KG quality has several dimensions, the exact definitions and distinctions being subject of dispute in the literature @wangKnowledgeGraphQuality2021. The importance of each dimension, depends on the usecase. We follow the methodology of @wangKnowledgeGraphQuality2021 and assess the @KG along the axes of accuracy, completeness, consistency, timeliness, trustworthiness and availability.

=== Accuracy
Accuracy describes the degree of factuality as well degree of conformity to the specification in our case, @RDF (syntactic validity).
Quantifying the accuracy requires ground truth data, which is unavailable by design. If it were available for parts of the graph, it would simply be incorporated and serve at most as a lower bound to accuracy.
Syntactic validity on the other hand is guaranteed by the current set of data ingestion methods, as incorrectly formatted data is discarded to preserve validity.
This is subject to change with integration of less well formatted data sources.


=== Consistency
Consistency is a measure of in graph contradictions.





// - comparison to trueprice reports
// - graph itself (wang21)
// - query translation

= Discussion

// discourages reporting
// - usefulness
// - shortcomings
// - future work
//   - product level
//   - text integration
//   - better pricing
//   - better category mapping


= Appendix
#set heading(numbering: "A", supplement: [Appendix])
#counter(heading).update(0)

= Graph Schema <appendix_schema>

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



