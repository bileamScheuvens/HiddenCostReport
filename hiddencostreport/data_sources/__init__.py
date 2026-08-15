from .wikirate import (
    parse_companies,
    parse_metrics_metadata,
    parse_metrics,
    example_metrics_metadata,
    example_metric,
    example_companies,
)
from .openproductsfacts import parse_openfoodfacts, parse_openproductsfacts
import networkx as nx
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph_manager import GraphManager


class Source:
    """
    Representation of single source for knowledge graph.
    Should provide name, description, and ideally schema by example of how a data point relates to the rest of the graph.
    Parse func should take graph manager and parse serialized or live data into rdf.
    """

    def __init__(
        self,
        name: str,
        parse_func: callable,
        active: bool = True,
        desc: str = "",
        example: nx.DiGraph = None,
        **load_kwargs,
    ):
        self.name = name
        self.active = active
        self._parse_func = parse_func
        self.load_kwargs = load_kwargs
        self.example = example

    def parse(self, graph: "GraphManager"):
        self._parse_func(graph, **self.load_kwargs)


SOURCES = [
    Source(
        name="Companies (Wikirate)",
        parse_func=parse_companies,
        desc="List of companies from wikirate.",
        example=example_companies(),
    ),
    Source(
        name="Metric Metadata (Wikirate)",
        parse_func=parse_metrics_metadata,
        desc="Wikirate metric metadata.",
        example=example_metrics_metadata(),
    ),
    # TODO make them individually adressable
    Source(
        name="Observations",
        parse_func=parse_metrics,
        desc="List of curated wikirate metric.",
        example=example_metric(),
    ),
    Source(
        name="openproductsfacts",
        parse_func=parse_openproductsfacts,
        desc="Product list from openPRODUCTfacts",
        active=False,
    ),
    Source(
        name="openfoodfacts",
        parse_func=parse_openfoodfacts,
        desc="Product list from openFOODfacts",
        active=False,
    ),
]
