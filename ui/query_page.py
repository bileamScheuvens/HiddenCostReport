import streamlit as st
from streamlit_searchbox import st_searchbox
from hiddencostreport.query_utils import get_emissions_by_name
from hiddencostreport.construct_graph import build_graph


st.write("Query")

def get_graph():
    graph, company_id_lookup = build_graph()
    return graph, company_id_lookup

graph, company_id_lookup = get_graph()
selected_company = st_searchbox(lambda x: "company_id_lookup")

st.write(get_emissions_by_name(graph, selected_company, company_id_lookup))

