from .wikirate import parse_companies, parse_metrics_metadata, parse_metrics
from .openproductsfacts import parse_productsfacts
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .graph_manager import GraphManager


class Source:

    def __init__(self, name: str, parse_func: callable, active: bool = True, desc: str = "", **load_kwargs):
        self.name = name
        self.active = active
        self._parse_func = parse_func
        self.load_kwargs = load_kwargs

    def parse(self, graph: "GraphManager"):
        self._parse_func(graph, **self.load_kwargs)

SOURCES = [
    Source(name="wr_companies", parse_func=parse_companies, desc="List of companies from wikirate."),
    Source(name="wr_metrics", parse_func=parse_metrics_metadata, desc="Wikirate metric metadata."),
    # TODO make them individually adressable
    Source(name="wr_curated_metrics", parse_func=parse_metrics, desc="List of curated wikirate metric."),
    Source(name="openproductsfacts", parse_func=parse_productsfacts, desc="Product list from Openproductsfacts"),
]
