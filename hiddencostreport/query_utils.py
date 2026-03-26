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
    return graph.query(query)


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


def query_get_revenue(company_id: str, year: int):
    return f"""
    SELECT ?value WHERE {{
    <{company_id}> <{NS}hasMetric> ?obs .
    ?obs <{NS}Value> ?value .
    ?obs <{NS}Year> {year} .
    ?obs <{NS}MetricID> ?metrID .
    ?metrID <{NS}MetricCategory> "revenue" .
    }}
    """


def query_transparent_company():
    return f"""
    SELECT ?company (COUNT(DISTINCT ?metric_category) AS ?metric_count) ?year WHERE {{
    ?companyID <{NS}Name> ?company .
    ?companyID <{NS}hasMetric> ?obs .

    VALUES ?metric_category {{ "water_recycled" "waste_hazardous" "emission_scope1" "waste" "water" "electricity_consumption" "emission" "emission_scope1" }}
    ?obs <{NS}Value> ?value .
    ?obs <{NS}Year> ?year .
    ?obs <{NS}MetricID> ?metrID .
    ?metrID <{NS}MetricTitle> ?metric_title .
    ?metrID <{NS}MetricCategory> ?metric_category .
    }}
    GROUP BY ?company 
    HAVING (COUNT(DISTINCT ?metric_category) > 0)
    """


def get_true_cost(graph: GraphManager, company: str, year: int):
    cost_calculator = TrueCostCalculator()

    id = graph.get_company_id(company)
    query = query_get_metrics(company_id=id, year=year)
    cost_lb, cost_ub = 0, 0
    for row in graph.query(query):
        bounds = cost_calculator.get_cost(
            metric_title=row["metrictitle"],
            metric_category=row["metriccategory"],
            metric_unit=row["unit"],
            metric_value=row["value"],
        )
        cost_lb += bounds[0]
        cost_ub += bounds[1]
    return cost_lb, cost_ub
