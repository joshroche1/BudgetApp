from fastapi import Depends

from sqlalchemy.orm import Session

from . import models, schema
from .database import SessionLocal



def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


async def get_budgetitems(db: Session = Depends(get_db)):
  budgetitems = db.query(models.BudgetItem).order_by(models.BudgetItem.id).all()
  return budgetitems

async def get_budgetitem(id: int, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == id).first()
  return budgetitem

async def get_items_for_budget(budgetid: int, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.budget == budgetid).all()
  return budgetitem

async def get_items_for_budget_by_type(bid: int, itemtype: str, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.budget == bid).filter(models.BudgetItem.itemtype == itemtype).all()
  return budgetitem

async def create_budgetitem(newname: str, newamount: str, newbudget: int, newitemtype: str, newcategory: str, newrecurrence: str, newrecurrence_day: int, db: Session = Depends(get_db)):
  if not newname:
    return {"error":"Name needed"}
  if not newamount:
    return {"error":"Value needed"}
  if not newbudget:
    newbudget = 1
  if not newitemtype:
    newitemtype = "Expense"
  if not newcategory:
    newcategory = "Other"
  if not newrecurrence:
    newrecurrence = "Monthly"
  if not newrecurrence_day:
    newrecurrence_day = 1
  budgetitem = models.BudgetItem(name=newname, amount=newamount, budget=newbudget, itemtype=newitemtype, category=newcategory, recurrence=newrecurrence, recurrence_day=newrecurrence_day)
  db.add(budgetitem)
  db.commit()
  return budgetitem

async def delete_budgetitem(id: int, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == id).first()
  if budgetitem is None:
    raise HTTPException(status_code=404, detail="BudgetItem not found")
  db.delete(budgetitem)
  db.commit()
  return {"message":"Successfully delete budgetitem item"}
