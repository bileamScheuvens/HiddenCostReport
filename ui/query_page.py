import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
from hiddencostreport.constants import NS
from app import get_graph


graph = get_graph()
st.write("company selection")
selected_company = st_searchbox(
    lambda x: graph.autocomplete_search(search_type="company", term=x)
)
if selected_company:
    id = graph.get_company_id(selected_company)
    st.write(f"company id: {id.split('#')[1]}")
query = st.text_area(
    "query",
    height=300,
    value="""\
PREFIX hcr: <http://hiddencostreport.org/schema#>
SELECT ?company ?metric ?value ?year WHERE {
    <{id}> hcr:Name ?company .
    <{id}> hcr:hasMetric ?obs .
    ?obs hcr:Value ?value .
    ?obs hcr:Year ?year .
    ?obs hcr:MetricID ?metrID .
    ?metrID hcr:MetricTitle ?metric .
} """,
)
submit = st.button("submit")


if submit and selected_company and query:
    query = query.replace("{id}", id)
    df = graph.query(query)
    if df.empty:
        st.title("Query returned no results")
    else:
        st.write(df)
