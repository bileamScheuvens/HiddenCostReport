
from .construct_graph import build_graph
from .constants import NS


def get_emissions_by_name(store, company, company_id_lookup={}):
    id = company_id_lookup[company]
    query = f"""
    SELECT ?company ?emissions ?year WHERE {{
    <{id}> <{NS}Name> ?company .
    <{id}> <{NS}hasMetric> ?m .
    ?m <{NS}Value> ?emissions .
    ?m <{NS}Year> ?year .
    }}
    """
    for row in store.query(query):
        print(f"{row['emissions']} tons in {row['year'].value}")




store, company_id_lookup = build_graph()
# store.optimize()
get_emissions_by_name(store,"nestle inc", company_id_lookup=company_id_lookup )

