import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
from hiddencostreport.constants import NS
from app import get_graph


graph = get_graph()
st.write("company selection")
selected_company = st_searchbox(lambda x: graph.autocomplete_search(search_type="company", term=x))
if selected_company:
    id = graph.get_company_id(selected_company)
    st.write(f"company id: {id.split('#')[1]}")
select = st.text_input("select", value="""\
SELECT ?metric ?value ?year""")
query = st.text_area(
        "query", 
        height=300,
        value="""\
WHERE {
<{id}> <{NS}Name> ?company .
<{id}> <{NS}hasMetric> ?obs .
?obs <{NS}Value> ?value .
?obs <{NS}Year> ?year .
?obs <{NS}MetricID> ?metrID .
?metrID <{NS}MetricTitle> ?metric .
} """)
submit = st.button("submit")



if submit and selected_company and select and query:
    query = query.replace("{id}", id)
    query = query.replace("{NS}", NS)
    selected_vars = select.replace("SELECT ", "").replace("?","").split()
    
    res = []
    for row in graph.query(select + " " + query):
        res.append(list(map(lambda x: x.value, row)))
    df = pd.DataFrame(res)
    if df.empty:
        st.title("Query returned no results")
    else:
        df.columns = selected_vars
        st.write(df)

