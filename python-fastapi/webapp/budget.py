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


def get_budgets(db: Session):
  budgetlist = db.query(models.Budget).all()
  return budgetlist

def get_budget(db: Session, bid):
  budget = db.query(models.Budget).filter(models.Budget.id == bid).first()
  return budget

def add_budget(db: Session, newbudget):
  budget = models.Budget(name=newbudget['name'], description=newbudget['description'])
  db.add(budget)
  db.commit()
  return budget

def delete_budget(db: Session, bid):
  budget = db.query(models.Budget).filter(models.Budget.id == bid).first()
  if budget is None:
    raise HTTPException(status_code=404, detail="Budget not found")
  db.delete(budget)
  db.commit()
  return True

def update_budget_field(db: Session, bid, field, newvalue):
  budget = db.query(models.Budget).filter(models.Budget.id == bid).first()
  if field == "name": 
    budget.name = newvalue
    db.commit()
  elif field == "description": 
    budget.description = newvalue
    db.commit()
  else: 
    return False
  return True

#