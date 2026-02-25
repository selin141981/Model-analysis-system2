"""
train_model.py — לוגיקת אימון מודל ושמירה

תפקיד:
1. קבלת dataframe + פרטים
2. הרצת preprocessing
3. המרה אוטומטית של עמודות טקסט למספרים
4. בחירת מודל ML
5. אימון
6. שמירת המודל + metadata
"""

import os
import json
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from part1.preprocess import preprocess

MODEL_MAP = {
    "linear": LinearRegression,
    "random_forest": RandomForestRegressor,
    "gradient_boost": GradientBoostingRegressor
}


def train_model_from_csv(df, feature_cols, label_col,
                         model_type, model_name, model_params,
                         column_types):
    """
    df           : DataFrame עם כל הנתונים
    feature_cols : רשימת שמות עמודות למאפיינים
    label_col    : שם העמודה הרצויה לחיזוי
    model_type   : "linear" / "random_forest" / "gradient_boost"
    model_name   : שם לשמירת המודל
    model_params : מילון פרמטרים למודל
    column_types : dict עם סוגי העמודות (למשל {"city": "categorical"})
    """

    pre_df = preprocess(df, column_types)

    X = pre_df[feature_cols]
    y = df[label_col]

    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()

    if categorical_cols:
        # ColumnTransformer עם One-Hot Encoding
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols)
            ],
            remainder="passthrough"
        )
    else:
        preprocessor = "passthrough"

    model_cls = MODEL_MAP[model_type]
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", model_cls(**model_params))
    ])

    model.fit(X, y)

    models_dir = "models"
    metadata_dir = "metadata"
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    model_path = f"{models_dir}/{model_name}.pkl"
    metadata_path = f"{metadata_dir}/{model_name}.json"

    joblib.dump(model, model_path)

    metadata = {
        "model_name": model_name,
        "model_type": model_type,
        "features": feature_cols,
        "label": label_col,
        "column_types": column_types,
        "categorical_cols": categorical_cols,
        "model_path": model_path
    }

    with open(metadata_path, "w", encoding="utf8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"Model trained and saved to {model_path}")
    print(f"Metadata saved to {metadata_path}")

    return metadata, model_path, metadata_path


if __name__ == "__main__":
    print("train_model.py מוכן לשימוש")
