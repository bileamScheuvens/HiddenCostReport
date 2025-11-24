
from .construct_graph import build_graph
from .constants import NS
#
# # run basic query
# query = f"""
# SELECT ?s ?o WHERE {{
# ?s <{ns}WikirateID> ?o .
# }}
# """
# for row in store.query(query):
#     print(row['s']


def get_emissions_by_name(store, company, company_id_lookup={}):
    id = company_id_lookup[company]
    query = f"""
    SELECT ?company ?emissions WHERE {{
    <{id}> <{NS}Name> ?company .
    <{id}> <{NS}hasMetric> ?m .
    ?m <{NS}Value> ?emissions
    }}
    """
    for row in store.query(query):
        print(row['emissions'])


store, company_id_lookup = build_graph()
get_emissions_by_name(store,"Nestle", company_id_lookup=company_id_lookup )

