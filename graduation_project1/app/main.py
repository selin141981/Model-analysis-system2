"""
הקובץ יוצר את שרת ה־FastAPI הראשי של הפרויקט ומחבר אליו את כל הנתיבים של אימון מודל
חיזוי ורשימת מודלים. בנוסף, הוא מגדיר נתיב בסיסי שמחזיר הודעה שמראה שה־API פעיל ורץ כראוי.

"""

from fastapi import FastAPI
from app.routers.train import router as train_router
from app.routers.predict import router as predict_router
from app.routers.models_list import router as models_router

app = FastAPI(
    title="ML API",
    version="1.0"
)

app.include_router(train_router)
app.include_router(predict_router)
app.include_router(models_router)


@app.get("/")
def root():
    return {"message": "ML API is running"}
