import re
import os
from collections import UserDict, defaultdict
from .constants import DATADIR

import json


class IDLookup(UserDict):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename

    def save(self):
        """Serialize store."""
        with open(os.path.join(DATADIR, f"{self.filename}.json"), "w") as f:
            f.write(json.dumps(self.data))

    def load(self):
        """Load serialized store."""
        loadpath = os.path.join(DATADIR, f"{self.filename}.json")
        if not os.path.exists(loadpath):
            return
        with open(loadpath, "r") as f:
            self.data = json.loads(f.read())


class CompanyIDLookup(IDLookup):
    """Dict wrapper for harmonized company names."""

    def __init__(self, *args, **kwargs):
        super().__init__(filename="company_id_lookup", *args, **kwargs)
        self.substitution_rules = {
            r"\.": "",
            r",": "",
            r"\bag\b": "",
            r"\bsa\b": "",
            r"\bcic\b": "",
            r"\bco(/)?(rp(oration)?)?\b": "",  # corporation
            r"\binc(orporated)?\b": "",  # incorporated
            r"\blimited\b": "",
            r"\b[pl]?[lt][cpdt]\b": "",  # plc llc ltd llt etc
            r"\(.*\)": "",
            r"[^\x00-\x7F]": "",  # any non ascii char
        }

    def sanitize_name(self, name: str) -> str:
        """Sanitize names by applying substitution rules."""
        name = name.lower()
        for pattern, sub in self.substitution_rules.items():
            name = re.sub(pattern, sub, name)
        return name.strip()

    def autocomplete_search(self, term: str) -> list[str]:
        term = self.sanitize_name(term)
        return [key for key in self.data if key.startswith(term)]

    def __contains__(self, key: str) -> bool:
        return self.sanitize_name(key) in self.data

    def __getitem__(self, key: str) -> str:
        return self.data[self.sanitize_name(key)]

    def __len__(self):
        return len(set(self.data.values()))

    def __setitem__(self, key: str, value: str) -> None:
        clean_name = self.sanitize_name(key)
        # pass if entire name was santized away
        if clean_name == "":
            return
        # handle new key
        if clean_name not in self.data:
            self.data[clean_name] = value
            return

        # handle attempted overwrite with different key. Indicates collision
        if self[clean_name] != value:
            raise ValueError(
                f"Naming conflict for {clean_name} derived from {key}. ID was {self[clean_name]}, trying to write {value}"
            )


class MetricIDLookup(IDLookup):
    """Dict wrapper for metric names."""

    def __init__(self, *args, **kwargs):
        super().__init__(filename="metric_id_lookup", *args, **kwargs)

    def autocomplete_search(self, term: str) -> list[str]:
        return [key for key in self.data if key.startswith(term)]


class CategoryMapper:
    # TODO: rewrite as function?

    def gri_to_trueprice(self, gri_designation: str):
        """(incomplete) manual mapping of global reporting initiative scores to trueprice categories."""
        mapping = {
            # 305 Emissions
            "305-1": "climate",
            "305-2": "climate",
            "305-3": "climate",
            "305-6": "airp_ozone",
            # 306 waste
            "306-1": "airp_ozone",
            # 408 child labor (only disclosure)
            # "408-1": "cl_haz",
            # 409 forced labor (only disclosure)
            # "409-1": "fl_workers_med",
        }
        mapping_default = defaultdict(lambda: None)
        for k, v in mapping:
            mapping_default[k] = v

    def _match_terms(self, target: str | float, terms: list[str]):
        """Shorthand for checking if target contains terms."""
        # Skip if target is NaN
        if isinstance(target, float):
            return False
        return any(term in target.lower() for term in terms)

    def derived_metrics(
        self, metric_designer, metric_title, questions, value_type, **kwargs
    ):
        if not self._match_terms(metric_title, ["per", "yearly change"]):
            return False
        return "derived"

    def emission_metrics(
        self, metric_designer, metric_title, questions, value_type, **kwargs
    ):
        if value_type != "Number":
            return False
        if not self._match_terms(metric_title, ["emission"]):
            return False
        category = "emission"
        if self._match_terms(metric_title, ["scope"]):
            category += "_scope_"
            for scope in ["1", "2", "3"]:
                if scope in metric_title:
                    category += scope
        return category

    def water_metrics(
        self, metric_designer, metric_title, questions, value_type, **kwargs
    ):
        if value_type != "Number":
            return False
        if not self._match_terms(metric_title, ["water"]):
            return False
        category = "water"
        if self._match_terms(metric_title, ["withdrawal"]):
            category += "_withdrawal"
        if self._match_terms(metric_title, ["recycled"]):
            category += "_recycled"
        return category

    def electricity_metrics(
        self, metric_designer, metric_title, questions, value_type, **kwargs
    ):
        if value_type != "Number":
            return False
        if not self._match_terms(metric_title, ["electricity", "energy", "power"]):
            return False
        return "electricity_consumption"

    def waste_metrics(
        self, metric_designer, metric_title, questions, value_type, **kwargs
    ):
        if value_type != "Number":
            return False
        if not self._match_terms(metric_title, ["waste"]):
            return False
        category = "waste"
        if self._match_terms(metric_title, ["non-hazardous"]):
            category += "_nonhazardous"
        elif self._match_terms(metric_title, ["hazardous"]):
            category += "_hazardous"
        if self._match_terms(metric_title, ["recycled"]):
            category += "_recycled"
        return category

    def disclosure_metrics(
        self, metric_designer, metric_title, questions, value_type, **kwargs
    ):
        if isinstance(metric_title, float):
            return False
        if not (
            self._match_terms(metric_title, ["disclos"])
            or self._match_terms(questions, ["disclos"])
        ):
            return False
        if value_type == "Number":
            return "disclosure_rate"
        else:
            return "disclosure_single"

    def revenue_metrics(
        self, metric_designer, metric_title, questions, value_type, **kwargs
    ):
        if value_type != "Money":
            return False
        if self._match_terms(metric_title, ["revenue"]):
            return "revenue"

    def assign_category(self, **kwargs):
        for mapper in [
            self.derived_metrics,
            self.disclosure_metrics,
            self.emission_metrics,
            self.water_metrics,
            self.electricity_metrics,
            self.waste_metrics,
            self.revenue_metrics,
        ]:
            res = mapper(**kwargs)
            if res:
                return res
        return "unmapped"
