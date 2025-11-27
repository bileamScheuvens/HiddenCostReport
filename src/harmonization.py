import re
from collections import UserDict

class CompanyIDLookup(UserDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def sanitize_name(self, name):
        name = name.lower()
        for pattern, sub in self.substitution_rules.items():
            name = re.sub(pattern, sub, name)
        return name.strip()

    def __contains__(self, key):
        return self.sanitize_name(key) in self.data

    def __getitem__(self, key):
        return self.data[self.sanitize_name(key)]

    def __setitem__(self, key, value):
        clean_name = self.sanitize_name(key)
        if clean_name == "":
            return
        if clean_name not in self.data:
            self.data[clean_name] = value
            return
            
        if self[clean_name] != value:
            raise ValueError(f"Naming conflict for {clean_name} derived from {key}. ID was {self[clean_name]}, trying to write {value}")
   
