"""
הקוד הזה מגדיר חיבור למסד נתונים SQLite בשם fastapi_tokens.db בעזרת SQL
הוא יוצר engine שמנהל את החיבור, מגדיר SessionLocal לעבודה עם הנתונים, ומכין Base שעליו יתבססו מחלקות המודל.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///fastapi_tokens.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()



