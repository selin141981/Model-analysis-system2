"""
הקוד מגדיר את מבנה הטבלה users במסד הנתונים באמצעות SQL.
"""

from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    tokens = Column(Integer, default=0)
