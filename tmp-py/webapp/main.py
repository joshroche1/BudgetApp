from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas, auth, accounts, budgets, transactions, users, weblists, exchangerates

### Initialization

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
messages = []
g = {}

def message(msg: str = ""):
  messages.append(msg)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


### VIEWS ###

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/login", response_class=HTMLResponse)
async def view_login_page(request: Request):
  messages.clear()
  return templates.TemplateResponse("login.html", {"request": request, "messages": messages, "g": g})

@app.post("/login", response_class=HTMLResponse)
async def view_login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
  messages.clear()
  token = auth.authenticate_user(db, username, password)
  loginuser = auth.get_user_by_email(db, username)
  g["token"] = token
  g["user"] = loginuser.email
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/logout", response_class=HTMLResponse)
async def view_logout(request: Request):
  messages.clear()
  g.clear()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/settings", response_class=HTMLResponse)
async def view_settings(request: Request, db: Session = Depends(get_db)):
  categorylist = weblists.get_weblist(db, "Category")
  currencylist = weblists.get_weblist(db, "Currency")
  accounttypelist = weblists.get_weblist(db, "AccountType")
  countrylist = weblists.get_weblist(db, "Country")
  userlist = users.list_users(db)
  exchangeratelist = exchangerates.list_exchangerates(db)
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categorylist": categorylist, "currencylist": currencylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "exchangeratelist": exchangeratelist, "userlist": userlist})

@app.get("/transactions", response_class=HTMLResponse)
async def view_transactions(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  transactionlist = transactions.list_transactions(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  categorylist = weblists.get_weblist(db, "Category")
  currencylist = weblists.get_weblist(db, "Currency")
  accounttypelist = weblists.get_weblist(db, "AccountType")
  countrylist = weblists.get_weblist(db, "Country")
  accountlist = accounts.list_accounts(db, skip=0, limit=1000, filterby="", filtervalue="", sortby="")
  return templates.TemplateResponse("transactions.html", {"request": request, "messages": messages, "g": g, "categorylist": categorylist, "currencylist": currencylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "accountlist": accountlist, "transactionlist": transactionlist})

@app.get("/accounts", response_class=HTMLResponse)
async def view_accounts(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  accountlist = accounts.list_accounts(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  currencylist = weblists.get_weblist(db, "Currency")
  accounttypelist = weblists.get_weblist(db, "AccountType")
  return templates.TemplateResponse("accounts.html", {"request": request, "messages": messages, "g": g, "accounttypelist": accounttypelist, "currencylist": currencylist, "accountlist": accountlist})

@app.get("/budgets", response_class=HTMLResponse)
async def view_budgets(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  budgetlist = budgets.list_budgets(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  currencylist = weblists.get_weblist(db, "Currency")
  return templates.TemplateResponse("budgets.html", {"request": request, "messages": messages, "g": g, "currencylist": currencylist, "budgetlist": budgetlist})

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
async def rest_create_account(request: Request, newentity: schemas.AccountCreate, db: Session = Depends(get_db)):
  entity = accounts.create_account(db, newentity)
  return entity

@app.post("/rest/account/add")
async def rest_add_account(request: Request, name: str = Form(...), description: str = Form(...), currency: str = Form(...), accounttype: str = Form(...), db: Session = Depends(get_db)):
  entity = accounts.add_account(db, name, description, accounttype, currency)
  return entity

@app.post("/rest/account/delete/{id}")
async def rest_delete_account(request: Request, id: int, db: Session = Depends(get_db)):
  result = accounts.delete_account(db, id)
  return result

#

@app.get("/rest/budget/")
async def rest_list_budget(request: Request, db: Session = Depends(get_db)):
  entitylist = budgets.list_budgets(db)
  return entitylist

@app.get("/rest/budget/{id}")
async def rest_get_account(request: Request, id: int, db: Session = Depends(get_db)):
  entity = budgets.get_budget(db, id)
  return entity
  
@app.post("/rest/budget/")
async def rest_create_account(request: Request, newentity: schemas.BudgetCreate, db: Session = Depends(get_db)):
  entity = budgets.create_budget(db, newentity)
  return entity

@app.post("/rest/budget/add")
async def rest_add_budget(request: Request, name: str = Form(...), description: str = Form(...), currency: str = Form(...), db: Session = Depends(get_db)):
  entity = budgets.add_budget(db, name, description, currency, 1)
  return entity

@app.post("/rest/budget/delete/{id}")
async def rest_delete_budget(request: Request, id: int, db: Session = Depends(get_db)):
  result = budgets.delete_budget(db, id)
  return result

#

@app.get("/rest/transaction/")
async def rest_list_transaction(request: Request, db: Session = Depends(get_db)):
  transactionlist = transactions.list_transactions(db)
  return transactionlist

@app.get("/rest/transaction/{id}")
async def rest_get_transaction(request: Request, id: int, db: Session = Depends(get_db)):
  entity = transactions.get_transaction(db, id)
  return entity
  
@app.post("/rest/transaction/")
async def rest_create_transaction(request: Request, newentity: schemas.TransactionCreate, db: Session = Depends(get_db)):
  entity = transactions.create_transaction(db, newentity)
  return entity

@app.post("/rest/transaction/add")
async def rest_add_transaction(request: Request, datetimestamp: str = Form(...), amount: str = Form(...), category: str = Form(...), currency: str = Form(...), name: str = Form(...), description: str = Form(...), accountid: str = Form(...), db: Session = Depends(get_db)):
  convertedvalue = float(amount)
  to_currency = accounts.get_account(db, int(accountid)).currency
  if str(currency) != str(to_currency):
    exrate = exchangerates.get_exchangerate_from_to(db, currency, to_currency)
    convertedvalue = float(amount)*float(exrate.rate)
  entity = transactions.add_transaction(db, datetimestamp, float(amount), convertedvalue, category, currency, name, description, accountid)
  return entity

@app.post("/rest/transaction/{id}/update/{fieldname}")
async def rest_update_transaction(request: Request, id: int, fieldname: str, fieldvalue: str = Form(...), db: Session = Depends(get_db)):
  entity = transactions.update_transaction_field(db, id, fieldname, fieldvalue)
  return entity

@app.post("/rest/transaction/delete/{id}")
async def rest_delete_transaction(request: Request, id: int, db: Session = Depends(get_db)):
  transaction = transactions.get_transaction(db, id)
  result = transactions.delete_transaction(db, id)
  return result

#

@app.get("/rest/user/")
async def rest_list_user(request: Request, db: Session = Depends(get_db)):
  entitylist = auth.get_users(db)
  return entitylist

@app.get("/rest/user/{id}")
async def rest_get_user(request: Request, id: int, db: Session = Depends(get_db)):
  entity = auth.get_user(db, id)
  return entity
  
@app.post("/rest/user/")
async def rest_create_user(request: Request, newentity: schemas.UserCreate, db: Session = Depends(get_db)):
  entity = auth.create_user(db, newentity)
  return entity

@app.post("/rest/user/add")
async def rest_add_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), passwordcheck: str = Form(...), db: Session = Depends(get_db)):
  if password != passwordcheck:
    return {"error":"Passwords must match"}
  entity = auth.add_user(db, username, email, password)
  return entity

@app.post("/rest/user/delete/{id}")
async def rest_delete_user(request: Request, id: int, db: Session = Depends(get_db)):
  result = auth.delete_user(db, id)
  return result

@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  token = auth.authenticate_user(db, form_data.username, form_data.password)
  return token

#

@app.get("/rest/weblist/")
async def rest_list_weblist(request: Request, db: Session = Depends(get_db)):
  entitylist = weblists.list_weblists(db)
  return entitylist

@app.get("/rest/weblist/{id}")
async def rest_get_weblist(request: Request, id: int, db: Session = Depends(get_db)):
  entity = weblists.get_weblist(db, id)
  return entity
  
@app.post("/rest/weblist/add")
async def rest_add_weblist(request: Request, newname: str = Form(...), newvalue: str = Form(...), db: Session = Depends(get_db)):
  entity = weblists.add_weblist(db, newname, newvalue)
  return entity

@app.post("/rest/weblist/delete/{id}")
async def rest_delete_weblist(request: Request, id: int, db: Session = Depends(get_db)):
  result = weblists.delete_weblist(db, id)
  return result

#

@app.get("/rest/exchangerate/")
async def rest_list_exchangerate(request: Request, db: Session = Depends(get_db)):
  entitylist = exchangerates.list_exchangerates(db)
  return entitylist

@app.get("/rest/exchangerate/{id}")
async def rest_get_exchangerate(request: Request, id: int, db: Session = Depends(get_db)):
  entity = exchangerates.get_exchangeratet(db, id)
  return entity
  
@app.post("/rest/exchangerate/add")
async def rest_add_exchangerate(request: Request, currency_from: str = Form(...), currency_to: str = Form(...), rate: str = Form(...), db: Session = Depends(get_db)):
  entity = exchangerates.add_exchangerate(db, currency_from, currency_to, rate)
  return entity

@app.post("/rest/exchangerate/delete/{id}")
async def rest_delete_exchangerate(request: Request, id: int, db: Session = Depends(get_db)):
  result = exchangerates.delete_exchangerate(db, id)
  return result

#