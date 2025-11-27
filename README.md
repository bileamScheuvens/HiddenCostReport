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
- UI
- Joining other datasources in rdf (wikidata)
- query translation



## Source Documentation:

### Wikirate
Repository of metrics and datasets linked to companies.

#### Method of integration:
CSVs parsed to rdf in schema from graph/schema.ttl



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




