# Negi Chen
# to transform datas (e.g. data cleaning, data normalize, data validated)
# Cleaned DataFrame (pandas + regex)

from ossaudiodev import control_names
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

    # rename words
    def _rename_columns(self, df: pd.DataFrame) ->pd.DataFrame:
        new_columns = []  #store new columns's name
        for col in df.columns:
            col_clean = col.strip().lower() #remove blank and turn into small namme
            if col_clean in self.alias:
                new_columns.append(self.alias[col_clean])
            else:
                new_columns.append(col) #otherwise stay original name
        df.columns = new_columns 
        return df

    #clean data
    def _strip_and_collapse(self, df: pd.DataFrame) ->pd.DataFrame:
        """
        for all string in the columns：
        1) convert values into strings
        2) replace NBSPs with normal spaces
        3) Trim leading and trailing spaces
        4) Merge multiple spaces, tabs, or newlines into a single space.
        """

        obj_cols = df.select_dtypes(include="object").columns
        for col in obj_cols:
            df[col] = df[col].astype(str)

            df[col] = df[col].str.replace("\u00A0", " ", regex=False)
            
            df[col] = df[col].str.strip()

            df[col] = df[col].str.replace(r"\s+", " ", regex=True)
        
        return df

# test
if __name__ == "__main__": 
    parser = HKJCparser() #call __init__
    print("\n--- Testing constructor ---");
    print("Alias mapping keys:", list(parser.alias.keys()));
    print("Required columns:", parser.required_columns);
    df = pd.DataFrame(columns = ["Horse Name", "Ranking", "YOF", "coach"])
    new_df = parser._rename_columns(df)
    print("Test new columns:", (list(new_df.columns)))
    data = {
        "Horse_name": ["  Romantic\u00A0Warrior  ", "  Equinox", None],
        "Sex": ["  male  ", "  GELDING ", "  F  "],
        "Rating": [" 123 (HK) ", " 129* ", "  117  "],  
        "Age": [6, 5, 4],  
    }
    df = pd.DataFrame(data)
    print("\n--- Before ---")
    print(df)
    clean_df = parser._strip_and_collapse(df.copy())
    print("\n--- After strip/collapse ---")
    print(clean_df)