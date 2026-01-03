import streamlit as st
from hiddencostreport.graph_manager import GraphManager

@st.cache_resource
def get_graph():
    return GraphManager()

front_page = st.Page("front_page.py", title="Hidden Cost Report")
query_page = st.Page("query_page.py", title="Query")
truecost_page = st.Page("truecost_page.py", title="True Cost")



pg = st.navigation([front_page, query_page, truecost_page])
pg.run()

