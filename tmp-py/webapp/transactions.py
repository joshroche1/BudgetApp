from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_transactions(db: Session, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = ""):
  if sortby == "name":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.name.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.name.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.name.asc()).offset(skip).limit(limit).all()
  elif sortby == "datetimestamp":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.datetimestamp.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.datetimestamp.asc().offset(skip).limit(limit)).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.datetimestamp.asc()).offset(skip).limit(limit).all()
  elif sortby == "amount":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.amount.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.amount.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.amount.asc()).offset(skip).limit(limit).all()
  elif sortby == "category":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.category.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.category.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.category.asc()).offset(skip).limit(limit).all()
  elif sortby == "currency":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.currency.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.currency.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.currency.asc()).offset(skip).limit(limit).all()
  else:
    return db.query(models.Transaction).order_by(models.Transaction.id.asc()).offset(skip).limit(limit).all()

def get_transaction(db: Session, id):
  entity = db.query(models.Transaction).filter(models.Transaction.id == id).first()
  return entity

def add_transaction(db: Session, newtransaction):
  entity = models.Transaction(name=newtransaction.name, description=newtransaction.description, amount=newtransaction.amount, currency=newtransaction.currency, category=newtransaction.category, datetimestamp=newtransaction.datetimestamp)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_transaction(db: Session, bid):
  entity = db.query(models.Transaction).filter(models.Transaction.id == bid).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True
