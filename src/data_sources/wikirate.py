from wikirate4py import API
from wikirate4py.models import Company
import dotenv
import os
from ..constants import ROOT

dotenv.load_dotenv(os.path.join(ROOT, ".env"))

wikirate = API(os.getenv("WIKIRATE_KEY"))


