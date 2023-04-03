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


@router.get("/budget/all", tags=["budget"])
async def get_budgets(db: Session = Depends(get_db)):
  budgets = db.query(models.Budget).order_by(models.Budget.id).all()
  return budgets

@router.get("/budget/id/{id}", tags=["budget"])
async def get_budget(id: int, db: Session = Depends(get_db)):
  budget = db.query(models.Budget).filter(models.Budget.id == id).all()
  return budget

@router.get("/budget/name/{name}", tags=["budget"])
async def get_budget_by_name(name: str, db: Session = Depends(get_db)):
  budget = db.query(models.Budget).filter(models.Budget.name == name).all()
  return budget

@router.post("/budget/create", tags=["budget"])
async def create_budget(newname: str, newowner: str, newcurrency: str, newnotes: str, db: Session = Depends(get_db)):
  if not newname:
    return {"error":"Name needed"}
  if not newowner:
    return {"error":"Value needed"}
  if not newcurrency:
    newcurrency = "USD"
  if not newnotes:
    newnotes = ""
  budget = models.Budget(name=newname, owner=newowner, currency=newcurrency, notes=newnotes)
  db.add(budget)
  db.commit()
  return budget

@router.post("/budget/delete/{id}", tags=["budget"])
async def delete_budget(id: int, db: Session = Depends(get_db)):
  budget = db.query(models.Budget).filter(models.Budget.id == id).first()
  if budget is None:
    raise HTTPException(status_code=404, detail="Budget not found")
  db.delete(budget)
  db.commit()
  return {"message":"Successfully delete budget item"}
