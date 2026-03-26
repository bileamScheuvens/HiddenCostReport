import streamlit as st
from collections import defaultdict
from streamlit_searchbox import st_searchbox
from hiddencostreport.cost_calculation import TrueCostCalculator
from plotly_charts import cost_sunburst
from hiddencostreport.query_utils import query_get_metrics, query_get_revenue
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

    query_result = graph.query(query_get_metrics(company_id=id, year=year))
    if not query_result.empty:
        query_result["bounds"] = query_result.apply(
            lambda row: cost_calculator.get_cost(
                metric_title=row["?metrictitle"],
                metric_category=row["?metriccategory"],
                metric_unit=row["?unit"],
                metric_value=row["?value"],
            ),
            axis=1,
        )
        for i, (c, t, bounds) in query_result[
            ["?metriccategory", "?metrictitle", "bounds"]
        ].iterrows():
            category_to_cost[c].append((t, bounds[0], bounds[1]))

        fig, total_hidden_cost = cost_sunburst(category_to_cost)
        st.plotly_chart(fig)

    product_price = st.number_input("Product Price", min_value=0)
    try:
        revenue = float(
            graph.query(query_get_revenue(company_id=id, year=year))["?value"][0]
        )
    except KeyError:
        revenue = None
    if product_price and revenue:
        st.write(f"Revenue in {year}: ${revenue:.2e}")
        st.write(f"Approximate total hidden cost: ${total_hidden_cost:.2e}")
        st.write(
            f"Proportional true cost: ${product_price + total_hidden_cost / revenue * product_price:.2f}"
        )
