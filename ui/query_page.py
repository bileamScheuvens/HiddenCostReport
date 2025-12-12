import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
from hiddencostreport.harmonization import GraphManager
from hiddencostreport.constants import NS


@st.cache_resource
def cached_graph():
    return GraphManager()


graph = cached_graph()
st.write("company selection")
selected_company = st_searchbox(lambda x: graph.autocomplete_search(search_type="company", term=x))
select = st.text_input("select", value="""\
SELECT ?metric ?value ?year""")
query = st.text_area("query", value="""\
WHERE {
<{id}> <{NS}Name> ?company .
<{id}> <{NS}hasMetric> ?obs .
?obs <{NS}Value> ?value .
?obs <{NS}Year> ?year .
?obs <{NS}MetricID> ?metrID .
?metrID <{NS}MetricTitle> ?metric .
} """)
submit = st.button("submit")

if selected_company:
    id = graph.get_company_id(selected_company)
    st.write(f"company id: {id.split('#')[1]}")


if submit and selected_company and select and query:
    query = query.replace("{id}", id)
    query = query.replace("{NS}", NS)
    selected_vars = select.replace("SELECT ", "").replace("?","").split()
    res = []
    for row in graph.query(select + " " + query):
        res.append(list(map(lambda x: x.value, row)))
    df = pd.DataFrame(res)
    df.columns = selected_vars
    st.write(df)

