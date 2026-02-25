"""
הקובץ משתמש בפונקציית החיבור שמוגדרת ב־database.py כדי לעבוד מול מסד הנתונים.
באמצעות חיבור זה הוא שומר לוגים של אימון וניבוי מודלים לצורך מעקב אחרי פעילות המערכת.
"""

from app.db.database import get_connection


def init_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usage_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        action TEXT,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


init_tables()


"""
הפונקציה log_training_action מתעדת במסד הנתונים פעולה של אימון מודל
"""


def log_training_action(model_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usage_logs(model_name, action) VALUES (?, ?)",
                (model_name, "train"))
    conn.commit()
    conn.close()


"""
הפונקציה log_prediction_action מתעדת במסד הנתונים פעולה של ניבוי
"""


def log_prediction_action(model_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usage_logs(model_name, action) VALUES (?, ?)",
                (model_name, "predict"))
    conn.commit()
    conn.close()