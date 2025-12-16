import streamlit as st
from app import get_graph
from hiddencostreport.data_sources import SOURCES

st.title("Hidden Cost Report")

graph = get_graph()

st.write("Sources to include:")
for source in SOURCES:
    is_active = st.toggle(label=source.name, value=True)
    source.active = is_active


rebuild_button = st.button("Rebuild Graph")

if rebuild_button:
    with st.status("rebuilding"):
        graph.rebuild_graph()

st.write(graph.graph_summary())
