import pandas as pd
import os


def read_costs():
    df = pd.read_excel(os.path.join(os.path.dirname(__file__), "Monetisation_factors", "20251121 MFDBOpenDatav4.0.2.xlsx"), sheet_name="MFDB open data")
    print(df)

