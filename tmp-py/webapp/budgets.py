from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_budgets(db: Session, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = ""):
  if sortby == "id":
    if filterby == "ownerid": return db.query(models.Budget).filter(models.Budget.ownerid == filtervalue).order_by(models.Budget.id.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Budget).order_by(models.Budget.id.asc()).offset(skip).limit(limit).all()
  elif sortby == "name":
    if filterby == "ownerid": return db.query(models.Budget).filter(models.Budget.ownerid == filtervalue).order_by(models.Budget.name.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Budget).order_by(models.Budget.name.asc()).offset(skip).limit(limit).all()
  else:
    return db.query(models.Budget).order_by(models.Budget.id.asc()).offset(skip).limit(limit).all()

def get_budget(db: Session, id):
  entity = db.query(models.Budget).filter(models.Budget.id == id).first()
  return entity

def add_budget(db: Session, newbudget):
  entity = models.Budget(name=newbudget.name, description=newbudget.description, ownerid=newbudget.ownerid)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_budget(db: Session, bid):
  entity = db.query(models.Budget).filter(models.Budget.id == bid).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True
