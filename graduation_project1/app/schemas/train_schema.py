"""
הקובץ train_schema.py מגדיר סכמות קלט עבור API של אימון מודל
פה בשביל לוודא שהקלט שנשלח ל־API כולל את כל הפרטים הדרושים לאימון
זה מבטיח שהנתונים שמגיעים ל־API תקינים ומסודרים.
"""

from pydantic import BaseModel
from typing import Dict, List


class TrainRequest(BaseModel):
    model_name: str
    model_type: str
    features: List[str]
    label: str
    column_types: Dict[str, str]
    model_params: Dict = {}