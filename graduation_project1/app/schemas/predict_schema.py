"""
הקובץ predict_schema.py מגדיר סכמת קלט עבור API של ניבוי
כלומר שכל הנתונים שצריכים להיכנס לחיזוי מגיעים בצורה מסודרת ותקנית.
"""

from pydantic import BaseModel


class PredictInput(BaseModel):
    root: dict