from fastapi import HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schema, config


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


def get_budgetitems(db: Session):
  budgetitemlist = db.query(models.BudgetItem).all()
  return budgetitemlist

def get_budgetitem(db: Session, bid):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == bid).first()
  return budgetitem

def add_budgetitem(db: Session, newbudgetitem):
  budgetitem = models.BudgetItem(name=newbudgetitem['name'], description=newbudgetitem['description'], amount=newbudgetitem['amount'], budgetid=newbudgetitem['budgetid'], category=newbudgetitem['category'], recurrence=newbudgetitem['recurrence'], recurrenceday=newbudgetitem['recurrenceday'])
  db.add(budgetitem)
  db.commit()
  return budgetitem

def delete_budgetitem(db: Session, bid):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == bid).first()
  if budgetitem is None:
    raise HTTPException(status_code=404, detail="BudgetItem not found")
  db.delete(budgetitem)
  db.commit()
  return True

def update_budgetitem_field(db: Session, bid, field, newvalue):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == bid).first()
  if field == "name": 
    budgetitem.name = newvalue
    db.commit()
  elif field == "description": 
    budgetitem.description = newvalue
    db.commit()
  elif field == "amount": 
    budgetitem.amount = newvalue
    db.commit()
  elif field == "budgetid": 
    budgetitem.budgetid = newvalue
    db.commit()
  elif field == "category": 
    budgetitem.category = newvalue
    db.commit()
  elif field == "recurrence": 
    budgetitem.recurrence = newvalue
    db.commit()
  elif field == "recurrenceday": 
    budgetitem.recurrenceday = newvalue
    db.commit()
  else: 
    return False
  return True
#

def get_budgetitems_by_budget(db: Session, bid):
  budgetitems = db.query(models.BudgetItem).filter(models.BudgetItem.budgetid == bid).order_by(models.BudgetItem.id).all()
  return budgetitems
#