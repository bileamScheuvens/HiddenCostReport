import os
from argparse import ArgumentParser
from .construct_graph import construct_graph
from .harmonization import GraphManager
from .query_utils import get_emissions_by_name
from streamlit import config as _config
from streamlit.web.bootstrap import run

parser = ArgumentParser(prog="HiddenCostReport")
parser.add_argument("command", default="ui", choices=["ui", "rebuild", "example_query"], help="Action to be performed.")
parser.add_argument("-v", "--verbose", default=0, action="count", dest="verbosity")
parser.add_argument("-i", "--interactive", dest="interactive", action="store_true")

args = parser.parse_args()


if args.command == "rebuild":
    construct_graph(verbosity=args.verbosity)
elif args.command == "ui":
    _config.set_option("server.headless", True)
    run(os.path.join("ui", "app.py"), args=[], flag_options=[], is_hello=False)
elif args.command == "example_query":
    graph = GraphManager()
    res = get_emissions_by_name(graph, "Nestle")
    print(*res, sep="\n")

if args.interactive:
    os.environ["PYTHONINSPECT"] = "TRUE"


