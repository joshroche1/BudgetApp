import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated

from . import models, schemas
from .database import SessionLocal

SECRET_KEY = "d32b45cb82372fd14777c09846af32cd65c9ba9f9fd48574c11c5a3ac56342fa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str


def hash_passwd(password: str):
  bytestr = str.encode(password)
  passhash = bcrypt.hashpw(bytestr, bcrypt.gensalt())
  return passhash

def get_user(db: Session, uid: int):
  return db.query(models.User).filter(models.User.id == uid).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, newuser: schemas.UserCreate):
  passhash = hash_passwd(newuser.password)
  entity = models.User(username=newuser.username, email=newuser.email, password=passhash)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def add_user(db: Session, newusername: str, newemail: str, newpassword: str):
  passhash = hash_passwd(newpassword)
  entity = models.User(username=newusername, email=newemail, password=passhash)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def update_user_password(db: Session, id: int, password: str):
  entity = db.query(models.User).filter(models.User.id == id).first()
  passhash = hash_passwd(password)
  entity.password = passhash
  db.persist(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_user(db: Session, uid: int):
  result = ""
  try:
    entity = db.query(models.User).filter(models.User.id == uid).first()
    db.delete(entity)
    db.commit()
    result = str(uid)
  except Exception as ex:
    result = str(ex)
  return result

def authenticate_user(db: Session, username: str, password: str):
  bpassword = str.encode(password)
  db_user = get_user_by_email(db, username)
  if db_user is None:
    raise HTTPException(status_code=400, detail="Username or password incorrect")
  passcheck = db_user.password
  if not bcrypt.checkpw(bpassword, passcheck):
    raise HTTPException(status_code=400, detail="Username or password incorrect")
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
  return Token(access_token=access_token, token_type="bearer")

def create_access_token(data: dict, expires_delta: timedelta):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception
  user = get_user_by_email(db, email=token_data.username)
  if user is None:
    raise credentials_exception
  return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
  return current_user

#