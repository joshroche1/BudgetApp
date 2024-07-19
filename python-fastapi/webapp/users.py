import bcrypt
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_users(db: Session):
  entitylist = db.query(models.User).order_by(models.User.id.asc()).all()
  return entitylist

def get_user(db: Session, id):
  entity = db.query(models.User).filter(models.User.id == id).first()
  return entity

def create_user(db: Session, newuser):
  passwd = bcrypt.hashpw(str.encode(newuser.password), bcrypt.gensalt())
  entity = models.User(username=newuser.username, email=newuser.email, password=passwd)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def add_user(db: Session, newusername, newemail, newpassword):
  passwd = bcrypt.hashpw(str.encode(newpassword), bcrypt.gensalt())
  entity = models.User(username=newusername, email=newuser.email, password=passwd)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_user(db: Session, id):
  entity = db.query(models.User).filter(models.User.id == id).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True
