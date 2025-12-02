from pyoxigraph import Store, NamedNode, Literal, Quad, BlankNode
import pandas as pd
from pandas.core.series import Series
import os
from ..constants import ROOT, DATADIR, NS


def parse_productsfacts(store: Store, filename: str = "openproductsfacts/en_openproductsfacts.csv", company_id_lookup: dict = {}):
    def _add_attribute(x: Series, product: NamedNode, key: str, label: str):
        """Add attribute to store with sanitization."""
        if pd.isna(x[key]):
            return
        for attr in x[key]:
            try:
                store.add(Quad(product, NamedNode(NS+label), NamedNode(NS + attr.replace(" ", "_"))))
            except ValueError:
                # TODO: log or treat invalid symbols. currently ~10 cases
                pass

    def _parse_product_row(x: Series):
        # construct name with prefix P for product
        product = NamedNode(NS + "P" + str(x["code"]))
        store.add(Quad(product, NamedNode(NS+"Name"), Literal(x["product_name"])))
        # TODO: Harmonize aliases for companies
        _add_attribute(x, product, key="brands_en", label="Brand")
        _add_attribute(x, product, key="ingredients_tags", label="Ingredient")
        _add_attribute(x, product, key="manufacturing_places", label="ManufacturedIn")
    
    products = pd.read_csv(os.path.join(DATADIR, filename), sep="\t", on_bad_lines="skip", low_memory=False)
    products.apply(_parse_product_row, axis=1)

