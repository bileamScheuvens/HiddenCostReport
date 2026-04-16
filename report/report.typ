#import "@preview/abbr:0.3.0"
#show: abbr.show-rule
#abbr.make(
  ("TCA", "True Cost Accounting"),
  ("API", "Application Program Interface"),
  ("SCC", "Social Cost of Carbon"),
  ("UNEP", "United Nations Environment Program"),
  ("TEEB", "The Economics of Ecosystems and Biodiversity"),
  ("NLP", "Natural Language Processing"),
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


= Introduction
Neglecting costs which affect third parties in economic transactions leads to false equilibria in price finding.
This not only reduces market efficiency but incentivizes unsustainable practices, by effectively subsidizing behavior that has hard to assess consequences.

To suppress this, one would have to consider (and assign costs to) all externalities relevant for the production of a good. Attempts at this difficult and time consuming practice are often called @TCA.

To illustrate what this looks like in practice, we may examine an existing report on the true price of coffee beans. For the specific brand of beans, @truepricecoffee estimates the true cost at around $9.33€"/ kg"$ compared to the market price of $8€$. The breakdown of the additional cost into categories can be seen in @tca_coffee.
In @sec_methodology we revisit this example with our proposed methodology.

This work investigates whether it is possible to automate this process at scale by aggregating and processing public data to arrive at an approximation of the true cost.
To this end we construct a temporal knowledge graph and categorize data sources into a predefined ontology. Each category is assigned a base unit and associated cost. Translating all metrics to costs yields a hidden cost per company, which, when put in relation to the revenue, allows for the very rough estimation of a true cost by product.
We term this approach @ATCA and provide a proof-of-concept implementation to facilitate further research and promote adoption of similar frameworks.


#figure(
  box(
    image("res/coffee_tca.png", width: 80%),
    clip: true,
    inset: (top: -2cm, bottom: -3.2cm),
  ),
  caption: [Example true cost calculation for coffee beans. #linebreak()
    Data from @truepricecoffee.],
) <tca_coffee>


// - explain why economics fails
// - explain rdf+sparql
// - explain price gap

== Related Work
Several works exist, which explore the concept of pricing displaced harm, yet to the best of our knowledge, none of them attempt automating this process end-to-end.

The True Price Foundation @truepricefoundation standardized and open-sourced a method for calculating a true price, which has been applied to different products such as @truepriceapple, @truepricefood, @truepricejeans, @truepricecoffee.

TEEBAgriFood @environmentTEEBAgriFoodEvaluationFramework2024 is part of the @TEEB intiative, which itself is part of the @UNEP.
It currently spans 14 countries and prices natural factors that are usually ignored in an attempt to influence policy making.

= Methodology <sec_methodology>
@tca_coffee presented the results of a proper true cost report by @truepricefoundation. Imagine how we might approach this same product without the ability to inspect the production chain or approach the company for additional information. Instead we rely on the incomplete data we have. For a given year we may know the revenue of _Bocca Coffee_ to be $\$ 6.9$ million.
For illustrative reasons, imagine we also know the emissions to be $100$ tonnes of $C O_2$ equivalent, alongside a water consumption of $6000 m^3$ and electricity consumption $100 M w h$.
We may then consult our table of costs per metric unit #footnote[for example obtained using the methodology of @truepricefoundation] to find the priced externalities from greenhouse gas emissions#footnote[sometimes abbreviated @SCC] at $312€$ / ton and water at $1.62€$ / $m^3$. For electricity we use the estimate by Sovacool2021 at $70€$ / $M w h$.
// TODO fix citation
The result of aggregating these externalities and breaking them down proportionally to a kilogram of beans can be seen in @tca_coffee_approx.

#figure(
  box(
    image("res/coffee_approx.png", width: 80%),
    clip: true,
    inset: (top: -2.8cm, bottom: -2.8cm),
  ),
  caption: [Example @ATCA result for Bocca Coffee Beans (left) compared to real data (right). ],
) <tca_coffee_approx>


The rest of this chapter explains the infrastructure needed to perform this approximation at scale.
At the core of this work lies the @KG, which the platform surrounding it attempts to make easily more accessible.
This section is therefore divided into graph construction and graph utilization.

== Graph Construction
The data ingestion phase is designed to be flexible and extensible to serve different use cases.
Inclusion of sources can be toggled in the interface. With the currently available sources graph construction and indexing is a matter of minutes on consumer hardware. This is subject to change with the inclusion of more or bottlenecked sources, such as those only available via @API.
After adding the schema (see @appendix_schema), each source is parsed into triples and stored using the graph database oxigraph @pellissiertanonOxigraph2026.

The availabe sources are described in the following.

=== Source: Wikirate
Wikirate @Wikirate is an open data platform, which crowdsources and hosts a variety of company data relating to @ESG issues.
Each data point regardless of type (Company, Metric, Project, Tag, Image, ...) lives in a shared namespace as so called cards, which can be fetched from an API.\
To include wikirate in the graph, a subset#footnote[This selection is done purely for scoping reasons. The source has a long tail of largely isolated and therefore less interesting data points.] of 1000 companies with most data points associated is selected, alongside the 1000 most bookmarked metrics.
These are cached and transformed from tabular format into triples, conforming to the schema described in @appendix_schema.


=== Source: OpenFoodFacts & OpenProductsFacts


=== Harmonization
With a diverse set of potential sources and in-source inconsistencies in data representation comes the burden of harmonizing the data, such that parts which reference the same conceptual entity are not disconnected.

Deciding on common vocabulary at data ingestion and enforcing the harmonized form throughout the graph lifetime ensures a baseline of interoperability.

Alongside cleanup of minor data quality issues, the most impactful harmonization steps in the pipeline are company name unification and metric categorization.


// TODO cite stemming
<name_unification>
To avoid ambiguity we introduce IDs for each Company. To obtain a map from all possible representations of company name to its ID, we draw inspiration from the @NLP technique of stemming to reduce a name down to a base form. Using regular expressions we strip away organizational indicators such as "inc." or "limited" and non-ascii characters.
We apply this to the name of the company and any known aliases and store the reduced forms in a lookup table mapping to the created ID.
Any collisions are recorded and either decided manually or discarded for the colliding aliases.
Access to the lookup table is then provided by checking for the equally sanitized form of the query term.
Conveniently the keys of the table can be used to generate company name completions in the user interface.

Metrics are also assigned an ID, however this is not enough to disambiguate. Metrics such as "Emission Scope 1" and "Scope 1 Emissions" clearly measure the same concept, but may have been collected by different parties or using different methodology.
It is therefore necessary to find a mapping between arbitrary metrics with name, value and unit to a known category as part of an ontology.
The proof-of-concept implementation uses a curated keyword matching approach for this. At the time of writing this only assigns a category to around $30%$ of metrics. There is a ceiling to the number of meaningful categories, as not every metric can be translated directly into a monetary value, however it is reasonable to believe that there is much room for improvement before this ceiling is reached.
One potential improvement would be querying an @LLM with the metric title and the task of assigning a category from the ontology. This approach is not error proof either, but with descriptive category names it is reasonable to believe it would perform and especially generalize better than a curated list of keywords.


Having described the data ingestion and processing pipeline we conclude this section with a vision of how to seamlessly utilize existing resources.

=== Integrating External Sources
@RDF supports the notion of federated queries. // TODO

= Graph Utilization
This chapter describes the way the @KG is made accessible to a user. Besides the included user-interface, a qlever endpoint is exposed which provide syntax highlighting, completion and execution analysis via the qlever-ui.
Lastly, to accomodate users unfamiliar with @SPARQL, querying in natural language is supported through @LLM based translation, directly from the command-line interface.

== UI
The user interface provides the core functionality for interacting with the @KG.
It first presents the user with the option to build the graph from a selection of sources, alongside a dropdown preview of relevant parts of the schema to help with orientation. @front_page shows this page.

#figure(image("res/front_page.png", width: 50%), caption: "Front page of the UI.")<front_page>

The next tab, seen in @query_page allows for direct query access of the graph.
It includes a searchbar for quick retrieval of Company IDs and a text field for query design.
Once submitted, the query is evaluated and the result is shown as a table and can additionally be downloaded in csv format.
Notably the access is read-only, exclusively allowing `SELECT` statements to prevent corruption of the @KG once fully constructed and indexed.

Upon first open, the query tab shows an example query, selecting all metrics for the selected company.
This demonstrates the schema applied in @SPARQL, provides a convenient namespace and demonstrates that graph construction was successful.


#figure(image("res/query_page.png", width: 50%), caption: "Query page of the UI with an example query.")<query_page>

Lastly the ui includes a tab for computing the true cost of a product given a company and year.
Once company and year are selected, the user is shown a breakdown of the metrics that were assigned a category with monetary equivalent. The are filterable by supercategory and aggregated to arrive at a total hidden cost estimate for the company in the given year.

Since the OpenProductsFacts dataset does not yet include a satisfactory level of coverage, the user is instead asked to provide just the price of a product of interest, which acts as a placeholder until OpenProductsFacts is well populated and integrated.
Given this, the revenue is retrieved and the hidden cost per dollar of revenue is computed to obtain the proportional true cost of the product of interest.

#figure(
  image("res/truecost_page.png", width: 80%),
  caption: "True cost page of the UI with an example selection.",
)<truecost_page>

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
Lastly one can qualitative judge the performance of the @LLM query translation component, as already explored in the previous chapter.


== True Cost Accuracy
Many existing @TCA reports (@environmentTEEBAgriFoodEvaluationFramework2024 @michalkeTrueCostAccounting2023a @truepricefood, @truepriceapple, @truepricejeans, @truepricecoffee) focus on a single product. Unfortunately the lack of data granularity makes this difficult to reproduce.
As a rough approximation we compute the hidden costs per dollar of revenue for a company and multiply this with the price of a product to get the hidden cost.
This approach has several assumptions which do not hold in practice:
- All products contribute to all metrics in proportion to their price.
- The entire supply chain is operated by the same company #footnote[There are inconsistencies between metrics, scope 2 and 3 emissions for example, account for external factors, while water usage only accounts for in house consumption.]
- The costs associated with metrics are location independent and constant.

@tca_coffee_approx demonstrates that an approximation using our methodology may at least be in the order of magnitude as a diligent true cost report, while highlighting some of the shortcomings, such as the fact that the approximation is more of a lower-bounding.
The scarce data landscape, both in the realm of true cost reports as well available supply chain data makes a rigorous assessment of our systems accuracy difficult. We excuse this with refererence to the fact, that this is a proof of concept implementation.

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
Timeliness describes whether the data in the graph is up-to-date with respect to the task. @wangKnowledgeGraphQuality2021
For the core task of @ATCA the bulk of the data, that is metrics and their values, fortunately does not grow stale, as it is strictly scoped to the year it was recorded for. It is rare that metric values change long after collection.
Company structure and product lineup do evolve. however the core mutates slowly enough, that outdated data is not of great concern.
The limitation instead lies in data collection upstream and with how recently it was fetched from there.
High timeliness is not of critical important to the task of @ATCA, nonetheless it is advised to limit attempts to a span of at least several years and at most several decades back in time to strike a balance between data abundance and staleness.


=== Trustworthiness
Trustworthiness describes how much the data can be trusted as objective and verifiable. @wangKnowledgeGraphQuality2021 It strongly correlated with, but distinct from accuracy in the sense that it has a subjective component in judgement of authority and credibility for data sources.
The @KG constructed in this work has a medium level of trustworthiness, since it includes crowdsourced and self reported data.
While often hard to validate, the data is unlikely to be completely false, as companies are likely to face consequences when consistently misreporting.


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

*Acknowledgements*\
The authors gratefully acknowledge the computing time granted by the KISSKI project. Some calculations for this research were conducted with computing resources under the project HiddenCostReport.

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



#pagebreak()

#bibliography("hiddencostreport.bib")



