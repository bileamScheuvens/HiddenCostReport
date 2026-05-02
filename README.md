## Hidden Cost Report
Tool for convenient information gathering on products / companies to inform decisions.
End goal is true cost calculation. Unlikely to be feasible with public information currently.
Approximate by priced exteralities per company  * fraction of revenue per product 

### For Full Description see [report](./report/report.pdf)

## Prototype scope:
[x] 1000 Companies (most data points as of 01/26)
[x] 1000 Metrics (most bookmarked as of 01/26)


## Source Documentation:

### Wikirate
Repository of metrics and datasets linked to companies.

#### Method of integration:
CSVs parsed to rdf in schema from graph/schema.ttl.
Metric automatically fetched from curated list.
Curation on the basis of relevance, novelty (no derived metrics like emissions per employee) and objectivity (no self reported targets).

### TruePriceMethod
Elaborate reports for true price of different goods in agriculture. Based in NL. Published their method with excel table of cost corresponding to finegrained metrics.

#### Method of integration
Their true prices are highly reliable but require detailed data, which is not provided by the publicly available sources.
Some GRI (global reporting intiative) categories can be translated to trueprice categories. Even then the available data is often just boolean disclosure rather than e.g. concrete 'number of years of forced labor under hazardous condition'.
Manual mapping of standards required.

### OpenProductsFacts
Crowdsourced DB of food items linked with ingredients, nutrients, packaging information and nutriscore.
Previously just OpenFoodFacts.

#### Method of integration:
Parsed from CSV.
(OpenFoodFacts has a partial rdf export, but the english locale is also in french.)\
Columns used:
- code 
- product_name 
- brands_en
- ingredients_tags
- manufacturing_places


