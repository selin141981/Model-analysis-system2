"""
preprocess.py — פונקציות ניקוי וטרנספורמציה

תפקיד:
1. המרת עמודות לפי סוג:
   - טקסט → get_dummies
   - תאריכים → המרה ל־datetime
   - מספרים → המרה ל־float
"""

import pandas as pd


def preprocess(df, column_types):
    df = df.copy()

    for col, typ in column_types.items():

        if typ == "numeric":
            df[col] = pd.to_numeric(df[col], errors="coerce")

        elif typ == "date":
            df[col] = pd.to_datetime(df[col], errors="coerce")

        elif typ == "category":
            df[col] = df[col].astype("category")

    df = pd.get_dummies(df, drop_first=True)

    return df