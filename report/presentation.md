---
marp: true
class: invert
paginate: true
math: mathjax
style: |
    .small-text {
        font-siz: 0.2em;
    }
    .textcolumns {
        display: grid;
        font-size: 0.8em;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
    }

---

<style>
  section {
        /* background-image: url('res/boschfooter.png'); */
        background-repeat: no-repeat;
        background-position: bottom 0px right;
        background-size: 100% 30px ;
    }
    ul {
        font-size: 0.8em;
    }
</style>

# HiddenCostReport
### _Open Data Fusion for Approximate True Cost Accounting using Knowledge Graphs_

<!-- // = Introduction -->
<!-- // -->
<!-- // - explain why economics fails -->
<!-- // - explain rdf+sparql -->
<!-- // -->
<!-- // -->
<!-- // = Related Work -->
<!-- // - teebagrifood -->
<!-- // - true price method -->
<!-- // -->
<!-- // = Methodology -->
<!-- // - graph construction -->
<!-- //   - sources -->
<!-- //   - harmonization -->
<!-- //     - manual cleanup -->
<!-- //   - categorization -->
<!-- // - graph utilization -->
<!-- //   - qlever -->
<!-- //   - ui -->
<!-- //   - query translation -->
<!-- // -->
<!-- // -->
<!-- // = Evaluation -->
<!-- // - comparison to trueprice reports -->
<!-- // - graph itself (wang21) -->
<!-- // - query translation -->
<!-- // -->
<!-- // = Discussion -->
<!-- // - usefulness -->
<!-- // - shortcomings -->
<!-- // - future work -->
<!-- //   - product level -->
<!-- //   - text integration -->
<!-- //   - better pricing -->
<!-- //   - better category mapping -->

<span style="color:grey"> Research Project by</span> 
<span style=""> Bileam Scheuvens</span>  <br>
<span style="color:grey"> under supervision of</span> 
<span style=""> Dr. Harry Scells</span> 

---

## Overview
- Situation - why this work is necessary
- What is TCA  
- Scaling
- 

---

## Situation
- price is a bad measure of societal value
    * unfair distribution
    * planned obsolescene
* the economy is reward hacking

--- 
![bg right width:16cm](res/coffee_tca.png)

## What is True Cost Accounting

* internalize everything
    * restoration 
    * compensation
    * retribution 
    * prevention of re-occurence
* tedious, difficult, temporary...
* can we do better?

---

## Why Health NLP lab?
![bg right width:16cm](res/HL3_filled.png)

* originally information retrieval
* now mostly data fusion & harmonization
* hopefully still interesting

---

## Scaling True Cost Accounting

* gather public data
* harmonize & categorize sources 
* assign costs
* build graph

---

## Data Ingestion
![bg right width:16cm](res/metric_ex.png)


* Selecting Sources
    - Wikirate
    - OpenProductsFacts
    - OpenFoodFacts
* harmonize



---

### Thanks for listening!
##### Questions, Notes, Ideas?
