"""
database.py — יצירת חיבור למסד נתונים SQLite

קובץ האחראי ליצירת חיבור אל מסד הנתונים מסוג כמו SQL
"""

import sqlite3


def get_connection():
    conn = sqlite3.connect("usage.db")
    return conn