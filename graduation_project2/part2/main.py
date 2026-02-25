"""
הקוד מגדיר שרת FastAPI שמנהל משתמשים ומערכת טוקנים.
פה אפשר להירשם ולהתחבר לקבלת טוקן גישה
כל קריאה ל־API בודקת את הטוקן של המשתמש ומחזירה את מספר הטוקנים שיש לו
יש נקודות שמאפשרות להוסיף טוקנים, לאמן מודל או לבצע חיזוי, כאשר כל פעולה מנכה טוקנים בהתאם
הסיסמאות נשמרות מוצפנות, והטוקנים נשמרים במסד נתונים SQLite.
"""


from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging

from database import SessionLocal, engine, Base
from models import User

logging.basicConfig(filename="server.log", level=logging.INFO)

SECRET_KEY = "simple-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=True
)

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    username: str
    password: str


class AddTokensRequest(BaseModel):
    amount: int


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        return False


def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token format")
        token = parts[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        tokens=0
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/tokens")
def tokens(current_user: User = Depends(get_current_user)):
    return {"tokens": current_user.tokens}


@app.post("/add_tokens")
def add_tokens(request: AddTokensRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.tokens += request.amount
    db.commit()
    return {"message": "Tokens added", "tokens": current_user.tokens}


@app.post("/train")
def train(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tokens < 1:
        raise HTTPException(status_code=403, detail="Insufficient tokens")
    current_user.tokens -= 1
    db.commit()
    return {"message": "Training done", "tokens": current_user.tokens}


@app.post("/predict")
def predict(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tokens < 5:
        raise HTTPException(status_code=403, detail="Insufficient tokens")
    current_user.tokens -= 5
    db.commit()
    return {"message": "Prediction done", "tokens": current_user.tokens}