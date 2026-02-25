"""
הקוד בודק אם המודל והמטא־דאטה שלו קיימים, טוען את המודל מהקובץ
ממיר את הקלט ל־DataFrame, מבצע חיזוי ומחזיר את התוצאה כ־JSON. אם משהו משתבש, הקובץ מחזיר שגיאה מתאימה.
"""

from fastapi import APIRouter, HTTPException
import os, joblib, json
import pandas as pd

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/{model_name}")
def predict(model_name: str, input_data: dict):
    try:
        model_path = os.path.join("models", f"{model_name}.pkl")
        metadata_path = os.path.join("metadata", f"{model_name}.json")

        if not os.path.exists(model_path) or not os.path.exists(metadata_path):
            raise HTTPException(status_code=404, detail="Model not found")

        model = joblib.load(model_path)

        with open(metadata_path, "r", encoding="utf8") as f:
            metadata = json.load(f)

        X = pd.DataFrame([input_data], columns=metadata["features"])

        prediction = model.predict(X)

        return {"prediction": prediction[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
