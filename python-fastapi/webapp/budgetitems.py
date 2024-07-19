from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_budgetitems(db: Session, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = ""):
  if sortby == "id":
    if filterby == "budgetid": return db.query(models.BudgetItem).filter(models.BudgetItem.budgetid == filtervalue).order_by(models.BudgetItem.id.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.BudgetItem).order_by(models.BudgetItem.id.asc()).offset(skip).limit(limit).all()
  elif sortby == "name":
    if filterby == "budgetid": return db.query(models.BudgetItem).filter(models.BudgetItem.budgetid == filtervalue).order_by(models.BudgetItem.name.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.BudgetItem).order_by(models.BudgetItem.name.asc()).offset(skip).limit(limit).all()
  else:
    return db.query(models.BudgetItem).order_by(models.BudgetItem.id.asc()).offset(skip).limit(limit).all()

def get_budgetitem(db: Session, id):
  entity = db.query(models.BudgetItem).filter(models.BudgetItem.id == id).first()
  return entity

def create_budgetitem(db: Session, newbudgetitem):
  entity = models.BudgetItem(name=newbudgetitem.name, description=newbudgetitem.description, amount=newbudgetitem.amount, category=newbudgetitem.category, recurrence=newbudgetitem.recurrence, duedate=newbudgetitem.duedate, budgetid=newbudgetitem.budgetid)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def add_budgetitem(db: Session, newname: str, newdescription: str, newamount: str, newcategory: str, newrecurrence: str, newduedate: str, newbudgetid: int):
  entity = models.BudgetItem(name=newname, description=newdescription, amount=newamount, category=newcategory, recurrence=newrecurrence, duedate=newduedate, budgetid=newbudgetid)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_budgetitem(db: Session, bid):
  entity = db.query(models.BudgetItem).filter(models.BudgetItem.id == bid).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True
