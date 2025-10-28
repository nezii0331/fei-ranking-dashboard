# Negi Chen
# to transform datas (e.g. data cleaning, data normalize, data validated)
# Cleaned DataFrame (pandas + regex)

import pandas as pd; #Python library used for working with tabular data (rows and columns), similar to Excel
import re;  #regex(search, match, and clean)
from typing import Dict, List, Optional;

class HKJCparser:
    """Parser for HKJC world ranking table."""

# This module cleans and standardizes the raw horse ranking data.
# It removes extra spaces, extracts numeric ratings, normalizes gender labels, and validates data quality.

    # python's constructor
    def __init__(self) -> None:
        # define mapping between English and Chinese column names
        self.alias = {
            "ranking": "Rank",
            "Horse Name": "Horse_name",
            "Horse": "Horse_name",
            "yof": "Age",
            "Sex": "Sex",
            "Coach": "Trainer",
            "coach": "Trainer", 
            "rating": "Rating",
            "trained": "Country",
            "surface": "Surface",
            "race": "Race_name"
        }

        # Define the final columns we want to keep (in order)
        self.required_columns = [
            "Rank", "Horse_name","Age","Sex", "Trainer", "Rating", "Country","Surface", "Race_name"
        ]

if __name__ == "__main__":
    parser = HKJCparser();
    print("\n--- Testing constructor ---");
    print("Alias mapping keys:", list(parser.alias.keys()));
    print("Required columns:", parser.required_columns);

