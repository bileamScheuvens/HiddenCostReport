import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
from hiddencostreport.constants import NS
from hiddencostreport.query_translation.translate import query_to_sparql
from app import get_graph


graph = get_graph()
st.write("company search")
selected_company = st_searchbox(
    lambda x: graph.autocomplete_search(search_type="company", term=x)
)
if selected_company:
    id = graph.get_company_id(selected_company)
    st.write(f"company id: {id.split('#')[1]}")

with st.sidebar:
    st.link_button("Open Qlever UI", "http://atca-qlever.health-nlp.com")

t_col1, t_col2 = st.columns(2, vertical_alignment="center")
with t_col1:
    txt2sparql = st.text_area(
        "text2sparql",
        placeholder="Natural Language Query to be translated...",
        height=10,
    )
with t_col2:
    translate = st.button("translate")


if "query" not in st.session_state:
    st.session_state["query"] = """\
PREFIX hcr: <http://hiddencostreport.org/schema#>
SELECT ?company ?metric ?value ?year WHERE {
    <{id}> hcr:Name ?company .
    <{id}> hcr:hasMetric ?obs .
    ?obs hcr:Value ?value .
    ?obs hcr:Year ?year .
    ?obs hcr:MetricID ?metrID .
    ?metrID hcr:MetricTitle ?metric .
} """


if translate:
    with st.spinner(text="Translating Query..."):
        translated, thought_process = query_to_sparql(txt2sparql)
        st.session_state["query"] = translated

query = st.text_area("query", height=300, value=st.session_state["query"])
submit = st.button("submit")


if submit and query:
    if selected_company:
        query = query.replace("{id}", id)
    if "INSERT" in query or "DELETE" in query:
        st.title("Graph is read only, no updates allowed.")
    else:
        df = graph.query(query)
        if df.empty:
            st.title("Query returned no results")
        else:
            st.write(df)
