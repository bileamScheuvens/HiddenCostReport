import streamlit as st
from hiddencostreport.graph_manager import GraphManager

@st.cache_resource
def get_graph():
    return GraphManager()

front_page = st.Page("front_page.py", title="Hidden Cost Report")
query_page = st.Page("query_page.py", title="Query")



pg = st.navigation([front_page, query_page])
pg.run()

