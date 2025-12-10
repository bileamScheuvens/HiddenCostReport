import streamlit as st
from streamlit_searchbox import st_searchbox
from hiddencostreport.harmonization import GraphManager
from hiddencostreport.constants import NS


@st.cache_resource
def cached_graph():
    return GraphManager()


graph = cached_graph()
st.write("company selection")
selected_company = st_searchbox(lambda x: graph.autocomplete_search(search_type="company", term=x))
query = st.text_area("query", value=""" SELECT ?company ?value ?metricname ?year WHERE {
<{id}> <{NS}Name> ?company .
<{id}> <{NS}hasMetric> ?m .
?m <{NS}Value> ?value .
?m <{NS}MetricName> ?metricname .
?m <{NS}Year> ?year .
} """)
submit = st.button("submit")

if selected_company:
    id = graph.get_company_id[selected_company]
    st.write(f"company id: {id.split('#')[1]}")


if submit and selected_company and query:
    query = query.replace("{id}", id)
    query = query.replace("{NS}", NS)
    for row in graph.query(query):
        st.write(f"company {row['company'].value}  \nmetric {row['metricname']}  \nvalue {row['value'].value}  \nyear {row['year'].value}  \n\n")
