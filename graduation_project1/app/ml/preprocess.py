"""
הקובץ preprocess.py אחראי על ניקוי והכנת נתונים לפני אימון או ניבוי של מודל
פה נוצר עותק של ה־DataFrame המקורי, ממירה עמודות למספרים, תאריכים או קטגוריות לפי הסוג שלהן
וזאת למטרה שכדי שהמודל יוכל להבין ולעבד את הנתונים בצורה נכונה
באימון מודל נדרש שמספרים יהיו בפורמט מספרי, תאריכים יהיו בפורמט datetime
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