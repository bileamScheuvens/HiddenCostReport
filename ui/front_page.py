import streamlit as st
from app import get_graph

st.write("Hidden Cost Report")

graph = get_graph()


rebuild_button = st.button("Rebuild Graph")

if rebuild_button:
    graph.rebuild_graph()

st.write(graph.graph_summary())
