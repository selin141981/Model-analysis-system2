# part1/run_part1.py

"""
הקוד הזה מריץ את החלק הראשון של הפרויקט – אימון מודל למידת מכונה על נתונים מקובץ CSV.
הקוד טוען נתונים מקובץ CSV, מפריד פיצ’רים ויעד, מבצע את כל מה שנדרש על מנת לאמן מודל.
 הוא מאמן מודל רגרסיה לינארית על הנתונים, שומר את המודל בקובץ pkl ואת המטא־דאטה בקובץ JSON, ומחזיר את הנתיבים של הקבצים.
"""

from app.ml.preprocess import preprocess
import os
import json
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

MODEL_MAP = {
    "linear": LinearRegression,
    "random_forest": RandomForestRegressor,
    "gradient_boost": GradientBoostingRegressor
}

def run_part1():
    """
    הפונקציה שמריצה את החלק הראשון – אימון מודל מהנתונים.
    """

    df = pd.read_csv("data/data.csv")
    feature_cols = [col for col in df.columns if col != "price"]
    label_col = "price"
    column_types = {}

    pre_df = preprocess(df, column_types)
    X = pre_df[feature_cols]
    y = df[label_col]

    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    if categorical_cols:
        preprocessor = ColumnTransformer(
            transformers=[("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols)],
            remainder="passthrough"
        )
    else:
        preprocessor = "passthrough"

    model_cls = MODEL_MAP["linear"]
    model = Pipeline([("preprocessor", preprocessor), ("regressor", model_cls())])
    model.fit(X, y)

    models_dir = "models"
    metadata_dir = "metadata"
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    model_path = f"{models_dir}/linear_model.pkl"
    metadata_path = f"{metadata_dir}/linear_model.json"
    joblib.dump(model, model_path)
    metadata = {
        "model_name": "linear_model",
        "features": feature_cols,
        "label": label_col
    }
    with open(metadata_path, "w", encoding="utf8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"Model trained and saved to {model_path}")
    print(f"Metadata saved to {metadata_path}")

    return model_path, metadata_path
