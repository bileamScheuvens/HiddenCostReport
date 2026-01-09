from .constants import NS
from .graph_manager import GraphManager
from .cost_calculation import TrueCostCalculator


def example_query(graph: GraphManager, company):
    id = graph.get_company_id(company)
    query = f"""
    SELECT ?company ?metric ?value ?year WHERE {{
    <{id}> <{NS}Name> ?company .
    <{id}> <{NS}hasMetric> ?obs .
    ?obs <{NS}Value> ?value .
    ?obs <{NS}Value> "No" .
    ?obs <{NS}Year> ?year .
    ?obs <{NS}Year> 2014 .
    ?obs <{NS}MetricID> ?metrID .
    ?metrID <{NS}MetricTitle> ?metric .
    }}
    """
    return [
        f"{row['company'].value} {row['metric'].value} {row['value'].value} {row['year'].value}"
        for row in graph.query(query)
    ]


def query_get_metrics(company_id: str, year: int):
    return f"""
    SELECT ?metrictitle ?metriccategory ?unit ?metricdesigner ?value WHERE {{
    <{company_id}> <{NS}hasMetric> ?obs .
    ?obs <{NS}Value> ?value .
    ?obs <{NS}Year> {year} .
    ?obs <{NS}MetricID> ?metrID .
    ?metrID <{NS}MetricTitle> ?metrictitle .
    ?metrID <{NS}Unit> ?unit .
    ?metrID <{NS}MetricCategory> ?metriccategory .
    ?metrID <{NS}MetricDesigner> ?metricdesigner .
    }}
    """


def query_transparent_company():
    return f"""
    SELECT ?company (COUNT(DISTINCT ?metric_category) AS ?metric_count) ?year WHERE {{
    ?companyID <{NS}Name> ?company .
    ?companyID <{NS}hasMetric> ?obs .

    VALUES ?metric_category {{ "emission_scope1" "waste" "water" "electricity_consumption" "emission" }}
    ?obs <{NS}Value> ?value .
    ?obs <{NS}Year> ?year .
    ?obs <{NS}MetricID> ?metrID .
    ?metrID <{NS}MetricTitle> ?metric_title .
    ?metrID <{NS}MetricCategory> ?metric_category .
    }}
    GROUP BY ?company ?year 
    HAVING (COUNT(DISTINCT ?metric_category) > 3)
    """


def get_true_cost(graph: GraphManager, company: str, year: int):
    cost_calculator = TrueCostCalculator()

    id = graph.get_company_id(company)
    query = query_get_metrics(company_id=id, year=year)
    cost_lb, cost_ub = 0, 0
    for row in graph.query(query):
        bounds = cost_calculator.get_cost(
            metric_title=row["metrictitle"].value,
            metric_category=row["metriccategory"].value,
            metric_unit=row["unit"].value,
            metric_value=row["value"].value,
        )
        cost_lb += bounds[0]
        cost_ub += bounds[1]
    return cost_lb, cost_ub
