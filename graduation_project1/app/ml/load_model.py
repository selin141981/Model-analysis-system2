"""
הקובץ load_model.py אחראי על טעינת מודל
ומידע נלווה שלו מהדיסק. הפונקציה מקבלת שם מודל, בודקת שקובץ המודל קיים, טוענת את המודל
ואת המטא־דאטה שלו ומחזירה את שניהם לשימוש בקוד.

"""
import os
import json
import joblib


def load_model_and_metadata(model_name):
    model_path = f"models/{model_name}.pkl"
    meta_path = f"metadata/{model_name}.json"

    if not os.path.exists(model_path):
        raise FileNotFoundError("Model not found")

    model = joblib.load(model_path)

    with open(meta_path, "r", encoding="utf8") as f:
        metadata = json.load(f)

    return model, metadata