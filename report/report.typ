#import "@preview/abbr:0.3.0"
#show: abbr.show-rule
#abbr.make(
  ("TCA", "True Cost Accounting"),
  ("ESG", "Environmental Social and Governance"),
  ("OWL", "Web Ontology Language"),
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
//

*Acknowledgements*\
The authors gratefully acknowledge the computing time granted by the KISSKI project. Some calculations for this research were conducted with computing resources under the project HiddenCostReport.

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
This chapter describes the way the @KG is made accessible to a user. Besides the included user-interface, a qlever endpoint is exposed which provide syntax highlighting, completion and execution analysis via the qlever-ui.
Lastly, to accomodate users unfamiliar with @SPARQL, querying in natural language is supported through llm based translation, directly from the command-line interface.

== UI

== Qlever

== Query Translation
Translation of natural language is accomplished by zero-shot prompting an @LLM with a rough description of the schema, along with instructions to avoid empirically observed mistakes. The full preprompt can be found in @appendix_prompt.
The model tasked with this translation is a degree of freedom, during development the model "deepseek-r1-distill-llama-70b" hosted by the #link("https://kisski.gwdg.de/en/")[KISSKI] initiative was used, as it delivered decent reasoning capability while being cheap at inference, though a more capable model may be selected for better results.
Due to the number of potential queries and nondeterministic responses, quantitative assessment of said results proved difficult.
We instead offer qualitative remarks:

For simple retrieval the approach is mostly reliable, but it begins to struggle with nested queries or complex dependencies.
For example for the question "find companies that increased their emissions without loss of revenue in 2016" in one instance produced the sparql query:

```sparql
SELECT ?company ?emissionValue2016 ?revenueValue2016
WHERE {
  ?company hcr:hasMetric ?emission2016 ;
           hcr:hasMetric ?revenue2016 ;
           hcr:hasMetric ?emission2015 ;
           hcr:hasMetric ?revenue2015 .

  ?emission2016 hcr:MetricID ?emissionMetricID ;
             hcr:Year 2016 ;
             hcr:Value ?emissionValue2016 .

  ?revenue2016 hcr:MetricID ?revenueMetricID ;
              hcr:Year 2016 ;
              hcr:Value ?revenueValue2016 .

  ?emission2015 hcr:MetricID ?emissionMetricID ;
             hcr:Year 2015 ;
             hcr:Value ?emissionValue2015 .

  ?revenue2015 hcr:MetricID ?revenueMetricID ;
              hcr:Year 2015 ;
              hcr:Value ?revenueValue2015 .

  ?emissionMetricID hcr:MetricCategory "emission" ;
                   hcr:MetricID ?emissionMetricID .

  ?revenueMetricID hcr:MetricCategory "revenue" ;
                   hcr:MetricID ?revenueMetricID .

  FILTER (?emissionValue2016 > ?emissionValue2015 && ?revenueValue2016 >= ?revenueValue2015)
}
```
This is logically and syntactically correct, but since it contains self references of the metric IDs, which the @SPARQL engine interprets as the condition that a triple `metricID hasMetric metricID` exists, it returns no results.
One way to address these trivial errors would be an agentic setting, where the model can contiually query the @KG until the query has results or it has been verified that the required information is not present in the graph.
We leave this as future work.


= Evaluation
Evaluation of the system can be approached from several directions.
One can measure the initial target of approximating true cost, by comparing output to existing true cost report.
Secondly one can examine the graph on its own and apply traditional @KG quality measures.
Lastly one can qualitative judge the performance of the @LLM query translation component.


== True Cost Accuracy
Many existing @TCA reports (@environmentTEEBAgriFoodEvaluationFramework2024 @michalkeTrueCostAccounting2023a @truepricefood, @truepriceapple, @truepricejeans, @truepricecoffee) focus on a single product. Unfortunately the lack of data granularity makes this difficult to reproduce.
As a rough approximation we compute the hidden costs per dollar of revenue for a company and multiply this with the price of a product to get the hidden cost.
This approach has several assumptions which do not hold in practice:
- All products contribute to all metrics in proportion to their price.
- The entire supply chain is operated by the same company #footnote[There are inconsistencies between metrics, scope 2 and 3 emissions for example, account for external factors, while water usage only accounts for in house consumption.]
- The costs associated with metrics are location independent.

To approximate @truepricecoffee, we may examine a denim Brand such as Levi Strauss and compute the price gap from the available metrics.
// TODO move to intro. just

== @KG Assessment
@KG quality has several dimensions, the exact definitions and distinctions being subject of dispute in the literature @wangKnowledgeGraphQuality2021. The importance of each dimension, depends on the usecase. We follow the methodology of @wangKnowledgeGraphQuality2021 and assess the @KG along the axes of accuracy, completeness, consistency, timeliness, trustworthiness and availability.

=== Accuracy
Accuracy describes the degree of factuality as well degree of conformity to the specification in our case, @RDF (syntactic validity). @wangKnowledgeGraphQuality2021
Quantifying the accuracy requires ground truth data, which is unavailable by design. If it were available for parts of the graph, it would simply be incorporated and serve at most as a lower bound to accuracy.
Syntactic validity on the other hand is guaranteed by the current set of data ingestion methods, as incorrectly formatted data is discarded to preserve validity.
This is subject to change with integration of less well formatted data sources.

=== Completeness
Completeness describes how much of the data required for a particular task is present in the graph. @wangKnowledgeGraphQuality2021
The application at hand theoretically requires complete knowledge of the universe and one could state that technically the completeness of the @KG is exactly 0.
However for practical purpose we limit outselves to obtainable data and instead model companies and metrics as a bipartite graph.
Connecting each company to the metrics we have about it and computing the edge density gives us a measure that can meaningfully substite completeness.
At the time of writing, this density lies at $12.32%$ across the time of recording. When broken down to yearly level the density drops to $1.02%$.
Density this low, even after filtering for the most documented companies on wikirate, is alarming and severely limits the amount of companies that meaningful true price approximations can be made for.

To get a better picture, @metrics_per_company shows the head of the distribution of around 250 companies, while @companies_per_metric shows the opposite perspective: the number of companies that report a value for each metric.


#figure(
  box(image("res/metrics_per_company.png"), clip: true, inset: (bottom: -2.5cm, right: -75%, top: -1cm)),
  caption: "Number of Metrics per Company.",
) <metrics_per_company>

#figure(
  box(image("res/companies_per_metric.png"), clip: true, inset: (bottom: -2.5cm, right: -75%, top: -1cm)),
  caption: "Number of Companies per Metric.",
) <companies_per_metric>



=== Consistency
Consistency is a measure of in-graph contradictions. @wangKnowledgeGraphQuality2021
While some contradictions are to be expected due to the crowd sourced nature of the data landscape, a certain degree of consistency can be enforced through the ontology. For example, since the relationship between the metrics "emissions scope 1", "emissions scope 2" and "emissions scope 1 and 2 combined" is obvious and (once encoded in the ontology) a violation of this relationship could trigger self correction or alert to the need of intervention.
Since this behavior would depend on a complete and robust ontology we leave it as future work.


=== Timeliness
Timeliness describes whether the data in the graph is up-to-date. @wangKnowledgeGraphQuality2021


// - comparison to trueprice reports
// - graph itself (wang21)
// - query translation

= Discussion
This work attempted to explore whether it is possible to automatically calculate the holistict true price of any product across all industries just from publicly available metrics about the company that produces it.
At the time of writing it unfortunately has to be concluded, that this is the not the case.
Even for true price lower bounding and when tolerating the clearly violated assumptions the resulting values are simply too unreliable (often with volatility across orders of magnitude year over year) to be regarded as anything more than noise.

Nonetheless there is hope for this type of approach in the future. With more careful scoping, diligent reporting and inclusion of curated data it might well be possible to create a tool to inform decision-making both along a supply chain and for individual consumers.



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

= Query Translation Prompt <appendix_prompt>

#raw(
  "Your task is to translate natural language questions into SPARQL queries.

The knowledge base is comprised of several sources, most prominently wikirate metrics.
The sources are not all harmonized, avoid specific vocabulary (tons might be called tonnes elsewhere).
The schema of the knowledge graph is as follows:
PREFIX hcr: <http://hiddencostreport.org/schema#>

hcr:company_id hcr:Name companyName ;
    hcr:OpenCorporatesID openCorporatesID ;
    hcr:hasMetric _:metricObservation .
_:metricObservation hcr:MetricID metricID ;
    hcr:Value observationValue ;
    hcr:Year observationYear ;
hcr:MetricID hcr:MetricTitle metricTitle ;
    hcr:MetricDesigner MetricDesigner ;
    hcr:Unit unit ;
    hcr:ValueType valuetype ;
    hcr:MetricType metricType ;
    hcr:MetricCategory MetricCategory ;
    hcr:Questions questions ;

Refer to metrics by their category, the categories are:
derived
disclosure_rate
disclosure_single
electricity_consumption
emission
emission_scope_1
emission_scope_12
emission_scope_123
emission_scope_13
emission_scope_2
emission_scope_23
emission_scope_3
revenue
unmapped
waste
waste_hazardous
waste_hazardous_recycled
waste_nonhazardous
waste_nonhazardous_recycled
waste_recycled
water
water_recycled
water_withdrawal

Return a single code block denoted with ```.
Only use the provided predicates.
Include PREFIX in your query.
",
)



#bibliography("hiddencostreport.bib")



