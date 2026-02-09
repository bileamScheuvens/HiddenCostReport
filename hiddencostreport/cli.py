import asyncio
import os
import subprocess
from argparse import ArgumentParser

from streamlit import config as _config
from streamlit.web.bootstrap import run

from .constants import METRICSPATH
from .data_sources.scrape_utils import download_metrics
from .data_sources.truepricemethod import read_costs
from .eval.eval_completeness import eval_completeness
from .graph_manager import GraphManager
from .query_translation.translate import query_to_sparql_prettyprint
from .query_utils import get_true_cost, query_transparent_company

parser = ArgumentParser(prog="HiddenCostReport")
parser.add_argument(
    "command",
    default="ui",
    choices=[
        "ui",
        "rebuild",
        "download",
        "test_mapping",
        "example_query",
        "example_cost",
        "translate",
        "stats",
        "eval",
    ],
    help="Action to be performed.",
)
parser.add_argument("-v", "--verbose", default=0, action="count", dest="verbosity")
parser.add_argument("-i", "--interactive", dest="interactive", action="store_true")
parser.add_argument("-q", "--query", dest="query", default="")
parser.add_argument("--ignore-cache", dest="ignore_cache", action="store_true")
parser.add_argument("--restart-qlever", dest="restart_qlever", action="store_true")

args = parser.parse_args()


if args.command == "rebuild":
    graph = GraphManager()
    # graph.rebuild_graph(verbosity=args.verbosity)
    # graph.serialize()
    if args.restart_qlever:
        print("restarting qlever")
        os.chdir("qlever")
        for cmd in [
            "qlever index --overwrite-existing --parallel-parsing false",
            "qlever start --kill-existing-with-same-port",
        ]:
            res = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
            )
            print(res.stderr)


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
elif args.command == "download":
    asyncio.run(download_metrics(METRICSPATH, ignore_cache=args.ignore_cache))
elif args.command == "eval":
    graph = GraphManager()
    eval_completeness(graph)

if args.interactive:
    os.environ["PYTHONINSPECT"] = "TRUE"
