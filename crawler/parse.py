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

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract numeric rating from strings like '123 (HK)' or '125*'
        and convert to integer. If no number found, set as None.
        """
        if "Rating" not in df.columns:
            return df
        
        def extract_number(s):
            if pd.isna(s):   #if the value is None or NaN, return None
                return None
            m = re.search(r"\d+", str(s)) #search for the first sequence of digits #\d+ means [0-9] and one or more digits
            if m:
                return int (m.group()) #convert the sequence of digits to an integer
            else:
                return None   #if no number found, return None
        df["Rating"] = df["Rating"].apply(extract_number) #apply the function to the Rating column
        return df


    def _clean_sex(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize the sex column
        """

        if "Sex" not in df.columns:
            return df
        
        # CREATE A MAPPING TABLE
        mapping ={
            "male": "M", "m": "M",
            "female": "F", "f": "F", "filly": "F","mare": "F", 
            "gelding": "G", "g":"G", 
            "colt": "C", "c":"C",
        }

        def normalize_sex(s):
            if pd.isna(s):
                return None
            val = str(s).strip().lower()
            return mapping.get(val, s)

        #use method to normalize datas    
        df["Sex"] = df["Sex"].apply(normalize_sex)

        return df


    def numeric_safe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Safely convert numeric-like columns (Rank, Age, Rating) to integers.
        """

        numeric_cols = ["Ranking", "Age" ,"Rating"]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], error="coerce").astype("Int64")

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