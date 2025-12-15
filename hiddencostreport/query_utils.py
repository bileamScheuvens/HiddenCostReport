from .constants import NS
from .graph_manager import GraphManager



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
    return [f"{row['company'].value} {row['metric'].value} {row['value'].value} {row['year'].value}" for row in graph.query(query)]



