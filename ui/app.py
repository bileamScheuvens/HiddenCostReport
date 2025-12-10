import streamlit as st


front_page = st.Page("front_page.py", title="Hidden Cost Report")
query_page = st.Page("query_page.py", title="Query")


pg = st.navigation([front_page, query_page])
pg.run()

