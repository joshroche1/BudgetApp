import bcrypt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from . import models, schema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# token: str = Depends(oauth2_scheme)


#

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schema.UserCreate):
  hashed_password = hash_password(user.password)
  db_user = models.User(email=user.email, username=user.username, password=hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def update_user_email(db: Session, username: str, email: str):
  user = db.query(models.User).filter(models.User.username == username).first()
  user.email = email
  db.add(user)
  db.commit()
  return user

def update_user_password(db: Session, username: str, password: str):
  user = db.query(models.User).filter(models.User.username == username).first()
  user.password = hash_password(password)
  db.add(user)
  db.commit()
  return user

#
def hash_password(password: str):
  bytestr = str.encode(password)
  passhash = bcrypt.hashpw(bytestr, bcrypt.gensalt())
  return passhash

def authenticate_user(db: Session, username: str, password: str):
  bpassword = str.encode(password)
  db_user = get_user_by_username(db, username)
  if db_user.username.find(username) < 0:
    db_user = get_user_by_email(db, username)
    if db_user.email.find(username) < 0:
      raise HTTPException(status_code=400, detail="Username or password incorrect")
#  if not db_user.password == password:
  passcheck = db_user.password
  if not bcrypt.checkpw(bpassword, passcheck):
    raise HTTPException(status_code=400, detail="Username or password incorrect")
  return {"access_token":username, "token_type":"bearer", "username": username}

#
def fake_decode_token(token):
  return models.User(email="user@test.tst", username="user" + token, password="testTEST")

def get_current_user(token: str = Depends(oauth2_scheme)):
  user = fake_decode_token(token)
  return user

#