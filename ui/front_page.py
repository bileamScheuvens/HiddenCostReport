import streamlit as st
import streamlit.components.v1 as components
from app import get_graph
from hiddencostreport.data_sources import SOURCES
from pyvis.network import Network

st.title("Hidden Cost Report")

graph = get_graph()

st.write("Sources to include:")

for source in SOURCES:
    row = st.container(horizontal=True)
    is_active = row.toggle(label=source.name, value=True)
    source.active = is_active
    if source.example is not None:
        with st.expander("Show schema"):
            G = Network(height='600px', width='100%', directed=True)
            G.from_nx(source.example)
            components.html(G.generate_html(f"{source.name}.html"), height=600)



rebuild_button = st.button("Rebuild Graph")

if rebuild_button:
    with st.status("rebuilding"):
        graph.rebuild_graph()

st.write(graph.graph_summary())

