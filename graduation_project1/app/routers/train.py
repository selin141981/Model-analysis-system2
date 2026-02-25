"""
הקובץ הזה מגדיר נתיב ב־FastAPI לצורך אימון מודל דרך העלאת קובץ CSV
המשתמש שולח קובץ CSV עם הנתונים, בוחר עמודת יעד
ואת כל מה שמתבקש
ואז מאמן את המודל על הנתונים, ושומר את המודל ואת המטא־דאטה שלו בקבצים
ובסוף נשלחת הודעה אם זה הצליח. אם משהו משתבש, מחזיר שגיאה מתאימה.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
import os, joblib, json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


router = APIRouter(prefix="/train", tags=["Training"])

"""
הפונקציה מקבלת קובץ CSV עם נתונים, מאמנת עליו מודל לפי סוג שבחרנו
ומחזירה הודעה על הצלחה תוך שמירת המודל והמטא־דאטה שלו בקבצים.
"""


@router.post("/")
async def train_model_endpoint(file: UploadFile = File(...), target_column: str = "price", model_name: str = "linear_model", model_type: str = "linear"):
    try:
        df = pd.read_csv(file.file)

        feature_cols = [col for col in df.columns if col != target_column]

        MODEL_MAP = {
            "linear": LinearRegression,
            "random_forest": RandomForestRegressor,
            "gradient_boost": GradientBoostingRegressor
        }

        categorical_cols = df[feature_cols].select_dtypes(include=["object"]).columns.tolist()
        if categorical_cols:
            preprocessor = ColumnTransformer(
                transformers=[("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols)],
                remainder="passthrough"
            )
        else:
            preprocessor = "passthrough"

        model_cls = MODEL_MAP.get(model_type, LinearRegression)
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", model_cls())
        ])

        X = df[feature_cols]
        y = df[target_column]
        model.fit(X, y)

        os.makedirs("models", exist_ok=True)
        model_path = os.path.join("models", f"{model_name}.pkl")
        joblib.dump(model, model_path)

        os.makedirs("metadata", exist_ok=True)
        metadata = {
            "features": feature_cols,
            "categorical_cols": categorical_cols,
            "model_type": model_type,
            "model_path": model_path
        }
        metadata_path = os.path.join("metadata", f"{model_name}.json")
        with open(metadata_path, "w", encoding="utf8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)

        return {"status": "Model trained successfully", "metadata": metadata}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
