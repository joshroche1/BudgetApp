from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_accounts(db: Session, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = ""):
  if sortby == "id":
    return db.query(models.Account).order_by(models.Account.id.asc()).offset(skip).limit(limit).all()
  elif sortby == "name":
    return db.query(models.Account).order_by(models.Account.name.asc()).offset(skip).limit(limit).all()
  else: 
    return db.query(models.Account).order_by(models.Account.id.asc()).offset(skip).limit(limit).all()

def get_account(db: Session, id):
  entity = db.query(models.Account).filter(models.Account.id == id).first()
  return entity

def create_account(db: Session, newaccount):
  entity = models.Account(name=newaccount.name, description=newaccount.description)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def add_account(db: Session, newname: str, newdescription: str, newcurrency: str, newaccounttype: str):
  entity = models.Account(name=newname, description=newdescription, currency=newcurrency, accounttype=newaccounttype)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_account(db: Session, bid):
  entity = db.query(models.Account).filter(models.Account.id == bid).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True
