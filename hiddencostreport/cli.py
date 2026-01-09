import os
from argparse import ArgumentParser
from .graph_manager import GraphManager
from .query_utils import example_query, get_true_cost, query_transparent_company
from streamlit import config as _config
from streamlit.web.bootstrap import run
from .data_sources.truepricemethod import read_costs

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
        "stats",
    ],
    help="Action to be performed.",
)
parser.add_argument("-v", "--verbose", default=0, action="count", dest="verbosity")
parser.add_argument("-i", "--interactive", dest="interactive", action="store_true")

args = parser.parse_args()


if args.command == "rebuild":
    graph = GraphManager()
    graph.rebuild_graph(verbosity=args.verbosity)
elif args.command == "ui":
    _config.set_option("server.headless", True)
    run(os.path.join("ui", "app.py"), args=[], flag_options=[], is_hello=False)
elif args.command == "example_query":
    graph = GraphManager()
    res = example_query(graph, "Nestle")
    print(*res, sep="\n")
    # res = graph.query(query_transparent_company())
    # print(*[x["company"].value + " " + str(x["year"].value) for x in res], sep="\n")
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

if args.interactive:
    os.environ["PYTHONINSPECT"] = "TRUE"
