import streamlit as st
from collections import defaultdict
from streamlit_searchbox import st_searchbox
from hiddencostreport.cost_calculation import TrueCostCalculator
from plotly_charts import cost_sunburst
from hiddencostreport.query_utils import query_get_metrics
from app import get_graph


graph = get_graph()
cost_calculator = TrueCostCalculator()

st.write("Select company and year for true cost calculation:")
company_col, year_col = st.columns([5, 1], vertical_alignment="top")

with company_col:
    st.space()
    selected_company = st_searchbox(
        lambda x: graph.autocomplete_search(search_type="company", term=x)
    )
    if selected_company:
        id = graph.get_company_id(selected_company)

with year_col:
    year = st.selectbox("year", range(2025, 1970, -1), label_visibility="hidden")


if selected_company and year:
    id = graph.get_company_id(selected_company)

    # TODO: rewrite as tree?
    category_to_cost = defaultdict(list)

    for row in graph.query(query_get_metrics(company_id=id, year=year)):
        category = row["metriccategory"]
        title = row["metrictitle"]
        lb, ub = cost_calculator.get_cost(
            metric_title=title,
            metric_category=category,
            metric_unit=row["unit"],
            metric_value=row["value"],
        )
        category_to_cost[category].append((title, lb, ub))
    st.plotly_chart(cost_sunburst(category_to_cost))
