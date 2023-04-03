from fastapi import Depends, APIRouter
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from . import models, schema
from .database import SessionLocal


router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@router.get("/budgetitem/all", tags=["budgetitem"])
async def get_budgetitems(db: Session = Depends(get_db)):
  budgetitems = db.query(models.BudgetItem).order_by(models.BudgetItem.id).all()
  return budgetitems

@router.get("/budgetitem/id/{id}", tags=["budgetitem"])
async def get_budgetitem(id: int, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == id).all()
  return budgetitem

@router.get("/budgetitem/id/{id}", tags=["budgetitem"])
async def get_items_for_budget(budgetid: int, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.budget == budgetid).all()
  return budgetitem

@router.post("/budgetitem/create", tags=["budgetitem"])
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
  budgetitem = models.BudgetItem(name=newname, amount=newamount, budget=newbudget, itemtype=newitemtype, category=newcategory, recurrence=newrecurrence, recurrence_day=newrfecurrence_day)
  db.add(budgetitem)
  db.commit()
  return budgetitem

@router.post("/budgetitem/delete/{id}", tags=["budgetitem"])
async def delete_budgetitem(id: int, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == id).first()
  if budgetitem is None:
    raise HTTPException(status_code=404, detail="BudgetItem not found")
  db.delete(budgetitem)
  db.commit()
  return {"message":"Successfully delete budgetitem item"}
