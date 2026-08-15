import os
from warnings import warn
from openai import OpenAI
import dotenv
import re
from ..constants import ROOT

dotenv.load_dotenv(os.path.join(ROOT, ".env"))

BASE_URL = "https://chat-ai.academiccloud.de/v1"
MODEL = "deepseek-v4-flash-0731"
# MODEL = "qwen3-235b-a22b"

client = OpenAI(api_key=os.getenv("SAIA_KEY"), base_url=BASE_URL)

SYSTEM_PROMPT = """
Your task is to translate natural language questions into SPARQL queries.

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

Refer to metrics by their category, the categories are 
```
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
```


Return a single code block denoted with ``` and nothing else.
Only use the predicates
Include PREFIX in your query.
"""


def extract_sparql(x):
    if "```sparql" not in x:
        warn(f"no sparl code block found in {x}")
        return ""
    return x.split("```sparql")[1].split("```")[0]


def extract_thought(x):
    if "<think>" not in x:
        warn(f"no thought process found in {x}")
        return ""
    return x.split("<think>")[1].split("</think>")[0]


def query_to_sparql(query: str):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        model=MODEL,
    )
    response = response.choices[0].message.content
    translation = extract_sparql(response)
    thought_process = extract_thought(response)

    return translation, thought_process


def query_to_sparql_prettyprint(graph, query: str, verbosity: int):
    translated, thought_process = query_to_sparql(query)
    try:
        query_result = graph.query(translated)
    except SyntaxError as e:
        query_result = f"Query Errored: {e}"

    print(f"""
========================================
original query:\n{query}
========================================
llm output:\n{translated}
========================================
query result:\n{query_result}"
========================================
""")
    if verbosity:
        print(f"""
llm thought process:\n{thought_process}")
========================================
""")
