from .constants import DATADIR
import os
import pandas as pd
import pint
import warnings
import re

class TrueCostCalculator():

    def __init__(self):
        self.cost_table = pd.read_csv(os.path.join(DATADIR, "metric_categories.csv"), index_col="category")
        self.units = pint.UnitRegistry()
        self.substitution_rules = {
                r"metric\s*": "",
                r"\s*of\s*": "",
                r"co2\s*(equivalent|eq\.?)?": "", # co2 eq./equivalent
        }


    def sanitize_unit(self, raw_unit: str) -> str:
        """Sanitize unit by applying substitution rules."""
        unit = raw_unit.lower()
        for pattern, sub in self.substitution_rules.items():
            unit = re.sub(pattern, sub, unit)
        try:
            return self.units(unit)
        except pint.errors.UndefinedUnitError:
            warnings.warn(f"failed to interpret unit {unit}. Raw was {raw_unit}")
            return "invalid"

    def get_cost(self, metric_title: str, metric_category: str, metric_unit: str, metric_value: str):
        # TODO: resolve emission scopes. Not sure where this should take place
        if metric_category not in self.cost_table.index:
            # TODO: maybe warn or log?
            return 0,0
        unit = self.sanitize_unit(metric_unit)
        if unit == "invalid":
            return 0,0

        # TODO: move this check in some util function
        if metric_value == "Unknown":
            return 0,0

        category = self.cost_table.loc[metric_category]
        hidden_lb = category.true_cost_lb - category.cost
        hidden_ub = category.true_cost_ub - category.cost
        try:
            normalized = (float(metric_value) * unit).to(category.unit).magnitude
            return normalized*hidden_lb, normalized*hidden_ub
        except pint.errors.DimensionalityError:
            warnings.warn(f"failed to convert {unit} to {category.unit}.\nMetric was {metric_title}")
            return 0,0
        
