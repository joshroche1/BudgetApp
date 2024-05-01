from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas, accounts, budgets, transactions, users

### Initialization

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


### VIEWS ###

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.get("/transactions", response_class=HTMLResponse)
async def view_transactions(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  transactionlist = transactions.list_transactions(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  return templates.TemplateResponse("transactions.html", {"request": request, "transactionlist": transactionlist})

@app.get("/accounts", response_class=HTMLResponse)
async def view_accounts(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  accountlist = accounts.list_accounts(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  return templates.TemplateResponse("accounts.html", {"request": request, "accountlist": accountlist})

@app.get("/budgets", response_class=HTMLResponse)
async def view_budgets(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  budgetlist = budgets.list_budgets(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  return templates.TemplateResponse("budgets.html", {"request": request, "budgetlist": budgetlist})

### REST ###

@app.get("/rest/account/")
async def rest_list_account(request: Request, db: Session = Depends(get_db)):
  entitylist = accounts.list_accounts(db)
  return entitylist

@app.get("/rest/account/{id}")
async def rest_get_account(request: Request, id: int, db: Session = Depends(get_db)):
  entity = accounts.get_account(db, id)
  return entity
  
@app.post("/rest/account/")
async def rest_add_account(request: Request, newentity: schemas.AccountCreate, db: Session = Depends(get_db)):
  entity = accounts.add_account(db, newentity)
  return entity

@app.delete("/rest/account/delete/{id}")
async def rest_delete_account(request: Request, id: int, db: Session = Depends(get_db)):
  result = accounts.delete_account(db, id)
  return result


@app.get("/rest/budget/")
async def rest_list_budget(request: Request, db: Session = Depends(get_db)):
  entitylist = budgets.list_budgets(db)
  return entitylist

@app.get("/rest/budget/{id}")
async def rest_get_account(request: Request, id: int, db: Session = Depends(get_db)):
  entity = budgets.get_budget(db, id)
  return entity
  
@app.post("/rest/budget/")
async def rest_add_account(request: Request, newentity: schemas.BudgetCreate, db: Session = Depends(get_db)):
  entity = budgets.add_budget(db, newentity)
  return entity

@app.delete("/rest/budget/delete/{id}")
async def rest_delete_budget(request: Request, id: int, db: Session = Depends(get_db)):
  result = budgets.delete_budget(db, id)
  return result


@app.get("/rest/transaction/")
async def rest_list_transaction(request: Request, db: Session = Depends(get_db)):
  transactionlist = transactions.list_transactions(db)
  return transactionlist

@app.get("/rest/transaction/{id}")
async def rest_get_transaction(request: Request, id: int, db: Session = Depends(get_db)):
  entity = transactions.get_transaction(db, id)
  return entity
  
@app.post("/rest/transaction/")
async def rest_add_transaction(request: Request, newentity: schemas.TransactionCreate, db: Session = Depends(get_db)):
  entity = transactions.add_transaction(db, newentity)
  return entity

@app.delete("/rest/transaction/delete/{id}")
async def rest_delete_transaction(request: Request, id: int, db: Session = Depends(get_db)):
  transaction = transaction.get_transaction(db, id)
  result = transactions.delete_transaction(db, id)
  return result


@app.get("/rest/user/")
async def rest_list_user(request: Request, db: Session = Depends(get_db)):
  entitylist = users.list_users(db)
  return entitylist

@app.get("/rest/user/{id}")
async def rest_get_account(request: Request, id: int, db: Session = Depends(get_db)):
  entity = users.get_user(db, id)
  return entity
  
@app.post("/rest/user/")
async def rest_add_account(request: Request, newentity: schemas.UserCreate, db: Session = Depends(get_db)):
  entity = users.add_user(db, newentity)
  return entity

@app.delete("/rest/user/delete/{id}")
async def rest_delete_user(request: Request, id: int, db: Session = Depends(get_db)):
  result = users.delete_user(db, id)
  return result

#