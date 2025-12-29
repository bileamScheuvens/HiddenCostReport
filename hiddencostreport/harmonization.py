import re
import os
from collections import UserDict
from .constants import DATADIR 

import json

class IDLookup(UserDict):

    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename

    def save(self):
        with open(os.path.join(DATADIR, f"{self.filename}.json"), 'w') as f:
            f.write(json.dumps(self.data))

    def load(self):
        loadpath = os.path.join(DATADIR, f"{self.filename}.json")
        if not os.path.exists(loadpath):
            return
        with open(loadpath, 'r') as f:
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
                r"\bco(/)?(rp(oration)?)?\b": "", # corporation
                r"\binc(orporated)?\b": "", # incorporated
                r"\blimited\b": "",
                r"\b[pl]?[lt][cpdt]\b": "", # plc llc ltd llt etc
                r"\(.*\)": "",
                r"[^\x00-\x7F]": "", # any non ascii char
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
            raise ValueError(f"Naming conflict for {clean_name} derived from {key}. ID was {self[clean_name]}, trying to write {value}")

class MetricIDLookup(IDLookup):
    """Dict wrapper for metric names."""

    def __init__(self, *args, **kwargs):
        super().__init__(filename="metric_id_lookup", *args, **kwargs)

    def autocomplete_search(self, term: str) -> list[str]:
        return [key for key in self.data if key.startswith(term)]


class CategoryMapper():

    def emission_metrics(self, metric_designer, metric_title, questions, value_type, **kwargs):
        if value_type != "Number":
            return False
        if "emission" not in metric_title.lower():
            return False
        # TODO treat scopes
        return "emission"


    def water_metrics(self, metric_designer, metric_title, questions, value_type, **kwargs):
        if value_type != "Number":
            return False
        if not any(x in metric_title.lower() for x in ["water"]):
            return False
        # TODO: treat recycled 
        return "water"

    def electricity_metrics(self, metric_designer, metric_title, questions, value_type, **kwargs):
        if value_type != "Number":
            return False
        if not any(x in metric_title.lower() for x in ["electricity", "energy", "power"]):
            return False
        return "electricity"

    def waste_metrics(self, metric_designer, metric_title, questions, value_type, **kwargs):
        if value_type != "Number":
            return False
        if not any(x in metric_title.lower() for x in ["waste"]):
            return False
        # TODO: treat recycled
        return "waste"
    
    def disclosure_metrics(self, metric_designer, metric_title, questions, value_type, **kwargs):
        if isinstance(metric_title, float):
            return False
        if not any(x in metric_title.lower() for x in ["disclos"]):
            return False
        if value_type == "Number":
            return "disclosure_rate"
        else:
            return "disclosure_single"

    def assign_category(self, **kwargs):
        for mapper in [self.disclosure_metrics, self.emission_metrics, self.water_metrics, self.electricity_metrics, self.waste_metrics]:
            res = mapper(**kwargs)
            if res:
                return res
        return "unmapped"

