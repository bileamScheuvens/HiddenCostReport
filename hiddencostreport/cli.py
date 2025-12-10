import os
from argparse import ArgumentParser
from .construct_graph import build_graph
from streamlit import config as _config
from streamlit.web.bootstrap import run

parser = ArgumentParser(prog="HiddenCostReport")
parser.add_argument("command", default="ui", choices=["ui", "rebuild"], help="Action to be performed.")
parser.add_argument("-v", "--verbosity", default=0, type=float)

args = parser.parse_args()


if args.command == "rebuild":
    build_graph(verbosity=args.verbosity)
elif args.command == "ui":
    _config.set_option("server.headless", True)
    run(os.path.join("ui", "app.py"), args=[], flag_options=[], is_hello=False)




