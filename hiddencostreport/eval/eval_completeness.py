import pandas as pd
import plotly.express as px
from ..graph_manager import GraphManager

px.defaults.template = "plotly"

prefix = "PREFIX hcr: <http://hiddencostreport.org/schema#>"


class EvalQuery:
    def __init__(self, name, query, plot_args):
        self.name = name
        self.query = query
        self.plot_args = plot_args

    def run(self, graph: GraphManager):
        df = graph.query(prefix + self.query)
        df["?count"] = pd.to_numeric(df["?count"])
        return df


eval_queries = [
    EvalQuery(
        name="metrics_per_company",
        query="""
SELECT ?company (COUNT(DISTINCT ?metricid ) as ?count) WHERE {
        ?companyid hcr:Name ?company .
        ?companyid hcr:hasMetric ?obs .
        ?obs hcr:MetricID ?metricid .
} GROUP BY ?company ORDER BY DESC(?count)
""",
        plot_args={"x": "?company"},
    ),
    EvalQuery(
        name="metrics_per_company_per_year",
        query="""
SELECT ?company ?year (COUNT(DISTINCT ?metricid ) as ?count) WHERE {
        ?companyid hcr:Name ?company .
        ?companyid hcr:hasMetric ?obs .
        ?obs hcr:MetricID ?metricid .
        ?obs hcr:Year ?year
} GROUP BY ?company ?year ORDER BY DESC(?count)
""",
        plot_args={"x": "?company", "color": "?year", "barmode": "group"},
    ),
    EvalQuery(
        name="companies_per_metric",
        query="""
SELECT ?metrictitle (COUNT(DISTINCT ?companyid ) as ?count) WHERE {
        ?companyid hcr:Name ?company .
        ?companyid hcr:hasMetric ?obs .
        ?obs hcr:MetricID ?metricid .
		?metricid hcr:MetricTitle ?metrictitle .
} GROUP BY ?metrictitle ORDER BY DESC(?count)
""",
        plot_args={"x": "?metrictitle"},
    ),
    EvalQuery(
        name="companies_per_metric_per_year",
        query="""
SELECT ?metrictitle ?year (COUNT(DISTINCT ?companyid ) as ?count) WHERE {
        ?companyid hcr:Name ?company .
        ?companyid hcr:hasMetric ?obs .
        ?obs hcr:MetricID ?metricid .
		?metricid hcr:MetricTitle ?metrictitle .
        ?obs hcr:Year ?year
} GROUP BY ?metrictitle ?year ORDER BY DESC(?count)
""",
        plot_args={
            "x": "?metrictitle",
            "color": "?year",
            "barmode": "group",
        },
    ),
]


def eval_completeness(graph: GraphManager):
    dfs = {}
    for q in eval_queries:
        df = q.run(graph)
        dfs[q.name] = df
        fig = px.bar(df, y="?count", title=q.name, **q.plot_args)
        fig.update_layout(width=2000)
        fig.show()

    n_companies = len(dfs["metrics_per_company"])
    n_metrics = len(dfs["companies_per_metric"])
    # TODO maybe use max-min year, currently identical
    n_years = dfs["companies_per_metric_per_year"]["?year"].nunique()
    edges_company_metric = dfs["metrics_per_company"]["?count"].sum()
    edges_company_obs = dfs["metrics_per_company_per_year"]["?count"].sum()
    print(f"""
Density for {n_companies} companies, across {n_metrics} metrics: 
          {edges_company_metric / (n_companies * n_metrics):.4f}%
Total density across {n_years} years:
          {edges_company_obs / (n_companies * n_metrics * n_years):.4f}%
""")
