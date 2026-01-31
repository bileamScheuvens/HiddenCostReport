import os
from argparse import ArgumentParser
from .graph_manager import GraphManager
from .query_utils import example_query, get_true_cost, query_transparent_company
from streamlit import config as _config
from streamlit.web.bootstrap import run
from .data_sources.truepricemethod import read_costs
from .query_translation.translate import query_to_sparql_prettyprint

parser = ArgumentParser(prog="HiddenCostReport")
parser.add_argument(
    "command",
    default="ui",
    choices=[
        "ui",
        "rebuild",
        "test_mapping",
        "example_query",
        "example_cost",
        "translate",
        "stats",
    ],
    help="Action to be performed.",
)
parser.add_argument("-v", "--verbose", default=0, action="count", dest="verbosity")
parser.add_argument("-i", "--interactive", dest="interactive", action="store_true")
parser.add_argument("-q", "--query", dest="query", default="")

args = parser.parse_args()


if args.command == "rebuild":
    graph = GraphManager()
    graph.rebuild_graph(verbosity=args.verbosity)
    graph.serialize()
elif args.command == "ui":
    _config.set_option("server.headless", True)
    run(os.path.join("ui", "app.py"), args=[], flag_options=[], is_hello=False)
elif args.command == "example_query":
    graph = GraphManager()
    # res = example_query(graph, "Nestle")
    res = graph.query(query_transparent_company())
    print(res)
elif args.command == "example_cost":
    graph = GraphManager()
    res = get_true_cost(graph, "Nestle", 2022)
    print(f"hidden cost of {res[0]:.2f} to {res[0]:.2f} euro")
elif args.command == "stats":
    graph = GraphManager()
    print(graph.graph_summary())
elif args.command == "test_mapping":
    read_costs()
    pass
elif args.command == "translate":
    if not args.query:
        raise ValueError("translate needs --query option set.")
    graph = GraphManager()
    query_to_sparql_prettyprint(graph, args.query, args.verbosity)


if args.interactive:
    os.environ["PYTHONINSPECT"] = "TRUE"
