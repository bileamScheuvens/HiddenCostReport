import os
from typing import TYPE_CHECKING

import pandas as pd
from pandas.core.series import Series
from pyoxigraph import Literal, NamedNode, Quad, Store

from ..constants import DATADIR, NS
from ..harmonization import IDLookup

if TYPE_CHECKING:
    from .graph_manager import GraphManager


def parse_openproductsfacts(
    graph: "GraphManager",
    filename: str = "openfacts/en_openproductsfacts.csv",
    company_id_lookup: dict = {},
):
    return parse_openfacts(
        store=graph.store, filename=filename, company_id_lookup=graph.company_id_lookup
    )


def parse_openfoodfacts(
    graph: "GraphManager",
    filename: str = "openfacts/en.openfoodfacts.org.products.csv",
):
    return parse_openfacts(
        store=graph.store, filename=filename, company_id_lookup=graph.company_id_lookup
    )


def parse_openfacts(
    store: Store,
    filename: str,
    company_id_lookup: IDLookup,
):
    def _add_attribute(x: Series, product: NamedNode, key: str, label: str):
        """Add attribute to store with sanitization."""
        if pd.isna(x[key]):
            return
        for attr in x[key].split(","):
            try:
                store.add(
                    Quad(
                        product,
                        NamedNode(NS + label),
                        NamedNode(NS + attr.replace(" ", "_")),
                    )
                )
            except ValueError:
                # TODO: log or treat invalid symbols. currently ~10 cases in openproducts
                pass

    def _parse_product_row(x: Series):
        # construct name with prefix P for product
        product = NamedNode(NS + "P" + str(x["code"]))
        store.add(Quad(product, NamedNode(NS + "Name"), Literal(x["product_name"])))
        _add_attribute(x, product, key="brands_en", label="Brand")
        _add_attribute(x, product, key="ingredients_tags", label="Ingredient")
        _add_attribute(x, product, key="manufacturing_places", label="ManufacturedIn")

    # TODO: remember why low memory
    products = pd.read_csv(
        os.path.join(DATADIR, filename), sep="\t", on_bad_lines="skip", low_memory=False
    )
    # link to company where available
    for brand in products["brands_en"].unique():
        if pd.isna(brand):
            continue
        if brand in company_id_lookup:
            # TODO: find source for more brand -by-> company matches
            try:
                store.add(
                    Quad(
                        NamedNode(NS + brand.replace(" ", "_")),
                        NamedNode(NS + "byCompany"),
                        NamedNode(company_id_lookup[brand]),
                    )
                )
            except ValueError:
                # skip invalid symbols
                continue

    products.apply(_parse_product_row, axis=1)
