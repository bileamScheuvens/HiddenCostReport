import streamlit as st
from streamlit_searchbox import st_searchbox
from hiddencostreport.query_utils import get_emissions_by_name
from hiddencostreport.construct_graph import load_graph, load_idlookup
from hiddencostreport.constants import NS


@st.cache_resource
def cached_graph():
    return load_graph()

@st.cache_resource
def cached_idlookup():
    return load_idlookup()

graph = cached_graph()
company_id_lookup = load_idlookup()
st.write("company selection")
selected_company = st_searchbox(lambda x: company_id_lookup.autocomplete_search(x))
query = st.text_area("query", value=""" SELECT ?company ?value ?metricname ?year WHERE {
<{id}> <{NS}Name> ?company .
<{id}> <{NS}hasMetric> ?m .
?m <{NS}Value> ?value .
?m <{NS}MetricName> ?metricname .
?m <{NS}Year> ?year .
} """)
submit = st.button("submit")

if selected_company:
    id = company_id_lookup[selected_company]
    st.write(f"company id: {id.split('#')[1]}")


if submit and selected_company and query:
    query = query.replace("{id}", id)
    query = query.replace("{NS}", NS)
    for row in graph.query(query):
        st.write(f"company {row['company'].value}  \nmetric {row['metricname']}  \nvalue {row['value'].value}  \nyear {row['year'].value}  \n\n")
        # st.write(f"company {row['company'].value}")
# st.write(get_emissions_by_name(graph, selected_company, company_id_lookup))
