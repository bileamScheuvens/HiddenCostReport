import re
import os
from collections import UserDict
from .constants import DATADIR, GRAPHPATH
from pyoxigraph import Store

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

    def __contains__(self, key: str) -> bool:
        return self.sanitize_name(key) in self.data

    def autocomplete_search(self, term: str) -> list[str]:
        term = self.sanitize_name(term)
        return [key for key in self.data if key.startswith(term)]

    def __getitem__(self, key: str) -> str:
        return self.data[self.sanitize_name(key)]

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


class GraphManager():
    """Wrapper around graph store, which handles harmonized access and lookup tables."""

    def __init__(self, *args, **kwargs):
        self.store = Store(GRAPHPATH)
        self.company_id_lookup = CompanyIDLookup()
        self.company_id_lookup.load()
        self.metric_id_lookup = MetricIDLookup()
        self.metric_id_lookup.load()

    def add(self, *args, **kwargs):
        self.store.add(*args, **kwargs)

    def load(self, *args, **kwargs):
        self.store.load(*args, **kwargs)

    def query(self, *args, **kwargs):
        return self.store.query(*args, **kwargs)

    def clear(self):
        self.store.clear()

    def __len__(self):
        return len(self.store)

    def autocomplete_search(self, search_type: str, term: str):
        if search_type == "company":
            return self.company_id_lookup.autocomplete_search(term)
        elif search_type == "metric":
            return self.metric_id_lookup.autocomplete_search(term)
        else:
            raise NotImplementedError()

    def get_metric_id(self, metric_designer: str, metric_name: str) -> str:
        return self.metric_id_lookup[f"{metric_designer}+{metric_name}"]

    def set_metric_id(self, metric_designer: str, metric_name: str, id: str) -> None:
        self.metric_id_lookup[f"{metric_designer}+{metric_name}"] = id
    
    def get_company_id(self, company_name: str) -> str:
        return self.company_id_lookup[company_name]

    def set_company_id(self, company_name: str, id: str) -> None:
        self.company_id_lookup[company_name] = id

    def save(self):
        self.company_id_lookup.save()
        self.metric_id_lookup.save()

