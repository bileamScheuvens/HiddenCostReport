## Hidden Cost Report
Tool for convenient information gathering on products / companies to inform decisions.
End goal is actual hidden cost calculation. Unlikely to be feasible with public information currently.
As approximation, at least give more holistic picture beyond just price and quality.
Report should showcase exploitation of people and planet, broken laws, corporate ties and de facto monopolies.

## Preprocessing
- Index for companies and available sources
- tag / classify sources with unit measurement 
- approximate conversion to interesting metrics (true cost, cumulative years lost, ...)

## Report generation routine
- Specify product (maybe also just company)
    - Search (?)
    - Barcode
- Gather info on product and product class
- Gather info on manufacturer and parents
- Compile data from relevant sources
- Compute metrics
- Generate Report 



## Prototype scope:
100 Companies (most data points as of 11/25)
500 Metrics (with environmental tag, most bookmarked as of 11/25)


## Timeline:
12/25 - kickoff, research, categorization of sources
01/26 - final schema, graph construction
02/26 - text processing / news article integration
03/26 - minimal (t?)ui, search utilities, evaluation
04/26 - buffer
05/26 - Report

Other Milestones:
- [ ] UI
- [ ] Joining other datasources in rdf (wikidata)
- [ ] query translation
- [x] qlever integration
    - [x] wait for fix: current build broken in docker (https://github.com/qlever-dev/qlever-control/issues/238)
- [x] download schedule / overview 
- [ ] logging
- [ ] source categorization & cost map
     - [ ] integrate trueprice, then leave be
- [x] schema example diagram
- [x] source selection on rebuild
- [x] decide when to write report: march + april
- [ ] knowledge graph evaluation 
    - [ ] follow Wang21 and give statement for each axis



## Source Documentation:

### Wikirate
Repository of metrics and datasets linked to companies.

#### Method of integration:
CSVs parsed to rdf in schema from graph/schema.ttl.
Metric automatically fetched from curated list.
Curation on the basis of relevance, novelty (no derived metrics like emissions per employee) and objectivity (no self reported targets).

### TruePriceMethod
Elaborate reports for true price of different goods in agriculture. Based in NL. Published their method with excel table of cost corresponding to finely granular metrics.

#### Method of integration
Their true prices are highly reliable but require detailed data, which is not provided by the publicly available sources.
Some GRI (global reporting intiative) categories can be translated to trueprice categories. Even then the available data is often just boolean disclosure rather than e.g. concrete 'number of years of forced labor under hazardous condition'.
Manual mapping of standards required.


### OpenProductsFacts
Crowdsourced DB of food items linked with ingredients, nutrients, packaging information and nutriscore.
Previously just OpenFoodFacts.

#### Method of integration:
Parsed from CSV.
OpenFoodFacts has a partial rdf export, but the english locale is also in french.\
Columns used:
- code 
- product_name 
- brands_en
- ingredients_tags
- manufacturing_places


