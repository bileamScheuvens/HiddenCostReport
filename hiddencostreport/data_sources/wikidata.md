```
PREFIX hcr: <http://hiddencostreport.org/schema#>
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT *
WHERE {
  {
    SELECT ?company ?companyName ?ocID WHERE {
      ?company hcr:Name ?companyName .
      ?company hcr:OpenCorporatesID ?ocID .
    }
    LIMIT 50
  }
  
  SERVICE <https://query.wikidata.org/sparql> {
    ?wikidataCompany wdt:P1320 ?wdOCID .
  }
  
  FILTER(STRENDS(STR(?wdOCID), CONCAT("/", STR(?ocID))))
}
```
