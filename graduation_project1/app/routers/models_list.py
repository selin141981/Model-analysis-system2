"""
הקובץ הזה מגדיר נתיבי API ב־FastAPI עבור מודלים מאומנים
הוא מאפשר למשתמשים לקבל רשימה של כל המודלים הקיימים במערכת יחד עם פרטים עליהם
בקצרה הקובץ קורא את קבצים שנשמרו במערכת, אוסף את המידע ומחזיר אותו בצורה מסודרת כ־JSON.

"""

from fastapi import APIRouter
import os ,json
from datetime import datetime

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/")
def list_models():
    models = []
    metadata_dir = "metadata"
    if not os.path.exists(metadata_dir):
        return {"models": []}

    for file_name in os.listdir(metadata_dir):
        if file_name.endswith(".json"):
            path = os.path.join(metadata_dir, file_name)
            with open(path, "r", encoding="utf8") as f:
                metadata = json.load(f)
                created_at = datetime.fromtimestamp(os.path.getctime(path)).isoformat()
                models.append({
                    "model_name": metadata.get("model_name", file_name.replace(".json", "")),
                    "model_type": metadata.get("model_type", ""),
                    "features": metadata.get("features", []),
                    "label": metadata.get("label", metadata.get("features")[-1] if metadata.get("features") else ""),
                    "created_at": created_at
                })

    return {"models": models}








