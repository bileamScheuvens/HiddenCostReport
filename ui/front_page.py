import streamlit as st
from app import get_graph
from hiddencostreport.data_sources import SOURCES
import networkx as nx
from pyvis import network 
import matplotlib.pyplot as plt

st.title("Hidden Cost Report")

graph = get_graph()

st.write("Sources to include:")

for source in SOURCES:
    row = st.container(horizontal=True)
    is_active = row.toggle(label=source.name, value=True)
    source.active = is_active
    if source.example is not None:
        show_example = row.button("Show schema", key=source.name)
        if show_example:
            G = source.example
            fig, ax = plt.subplots()
            pos = nx.spring_layout(G)
            fig = nx.draw(G, pos, with_labels=True)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "label"))
            st.pyplot(fig)




rebuild_button = st.button("Rebuild Graph")

if rebuild_button:
    with st.status("rebuilding"):
        graph.rebuild_graph()

st.write(graph.graph_summary())


