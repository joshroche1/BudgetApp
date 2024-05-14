import datetime
from fastapi import Depends, FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from functools import lru_cache
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas, auth, config, accounts, budgets, transactions, users, weblists, exchangerates

### Initialization

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
messages = []
g = {}

@lru_cache
def get_settings():
  return config.Settings()

def message(msg: str = ""):
  messages.append(msg)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def parse_date(datetimestamp: str, dateformat: str):
  result = ""
  currentdate = datetime.datetime.now().strftime('%Y-%m-%d')
  try:
    if dateformat == "Y-m-d":
      tmp1 = datetimestamp.split('-')
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = str(tmp1[0]) + "-" + str(tmp1[1]) + "-" + str(tmp1[2])
    elif dateformat == "Y/m/d":
      tmp1 = datetimestamp.split("/")
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = str(tmp1[0]) + "-" + str(tmp1[1]) + "-" + str(tmp1[2])
    elif dateformat == "Y.m.d":
      tmp1 = datetimestamp.split(".")
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = str(tmp1[0]) + "-" + str(tmp1[1]) + "-" + str(tmp1[2])
    elif dateformat == "d.m.y":
      tmp1 = datetimestamp.split(".")
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = "20" + str(tmp1[2]) + "-" + str(tmp1[1]) + "-" + str(tmp1[0])
    else:
      return currentdate
  except Exception as ex:
    print(str(ex))
    result = currentdate
  return result

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
  messages.clear()
  categorylist = weblists.get_weblist(db, "Category")
  currencylist = weblists.get_weblist(db, "Currency")
  accounttypelist = weblists.get_weblist(db, "AccountType")
  countrylist = weblists.get_weblist(db, "Country")
  userlist = users.list_users(db)
  exchangeratelist = exchangerates.list_exchangerates(db)
  settings = get_settings()
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categorylist": categorylist, "currencylist": currencylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "exchangeratelist": exchangeratelist, "userlist": userlist, "settings": settings})

@app.get("/transactions", response_class=HTMLResponse)
async def view_transactions(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  messages.clear()
  transactionlist = transactions.list_transactions(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  categorylist = weblists.get_weblist(db, "Category")
  currencylist = weblists.get_weblist(db, "Currency")
  accounttypelist = weblists.get_weblist(db, "AccountType")
  countrylist = weblists.get_weblist(db, "Country")
  accountlist = accounts.list_accounts(db, skip=0, limit=1000, filterby="", filtervalue="", sortby="")
  return templates.TemplateResponse("transactions.html", {"request": request, "messages": messages, "g": g, "categorylist": categorylist, "currencylist": currencylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "accountlist": accountlist, "transactionlist": transactionlist})

@app.get("/accounts", response_class=HTMLResponse)
async def view_accounts(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  messages.clear()
  accountlist = accounts.list_accounts(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  currencylist = weblists.get_weblist(db, "Currency")
  accounttypelist = weblists.get_weblist(db, "AccountType")
  return templates.TemplateResponse("accounts.html", {"request": request, "messages": messages, "g": g, "accounttypelist": accounttypelist, "currencylist": currencylist, "accountlist": accountlist})

@app.get("/budgets", response_class=HTMLResponse)
async def view_budgets(request: Request, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = "", db: Session = Depends(get_db)):
  messages.clear()
  budgetlist = budgets.list_budgets(db, skip=skip, limit=limit, filterby=filterby, filtervalue=filtervalue, sortby=sortby)
  currencylist = weblists.get_weblist(db, "Currency")
  return templates.TemplateResponse("budgets.html", {"request": request, "messages": messages, "g": g, "currencylist": currencylist, "budgetlist": budgetlist})

@app.post("/transactions/importfile", response_class=HTMLResponse)
async def view_transactions_importfile(request: Request, uploadfile: UploadFile = File(...), db: Session = Depends(get_db)):
  messages.clear()
  result = {}
  importarr = []
  try:
    fileread = await uploadfile.read()
    filecontents = str(fileread, 'iso-8859-1')
    for tmpline in filecontents.split("\n"):
      tmparr = tmpline.split(",")
      importarr.append(tmparr)
    result["filename"] = uploadfile.filename
    result["contenttype"] = uploadfile.content_type
    result["headers"] = uploadfile.headers
    result["size"] = uploadfile.size
    result["contents"] = filecontents
    result["error"] = ""
  except Exception as ex:
    result["error"] = str(ex)
  currencylist = weblists.get_weblist(db, "Currency")
  accountlist = accounts.list_accounts(db, skip=0, limit=1000, filterby="", filtervalue="", sortby="")
  return templates.TemplateResponse("importfile.html", {"request": request, "messages": messages, "g": g, "result": result, "importarr": importarr, "filecontents": filecontents, "currencylist": currencylist, "accountlist": accountlist})

@app.post("/transactions/importdata", response_class=HTMLResponse)
async def view_transactions_importdata(request: Request, import_datetimeformat: str = Form(...), import_accountid: str = Form(...), import_currency: str = Form(...), datetimefield: str = Form(...), namefield: str = Form(...), descriptionfield: str = Form(...), amountfield: str = Form(...), categoryfield: str = Form(...), importeddata: str = Form(...), db: Session = Depends(get_db)):
  messages.clear()
  result = ""
  datetime_col = int(datetimefield)-1
  name_col = int(namefield)-1
  description_col = int(descriptionfield)-1
  amount_col = int(amountfield)-1
  category_col = int(categoryfield)-1
  acctid = int(import_accountid)
  to_currency = accounts.get_account(db, acctid).currency
  exrate = 1.0
  if import_currency != str(to_currency):
    exchangerate = exchangerates.get_exchangerate_from_to(db, currency, to_currency)
    exrate = exchange.rate
  try:
    tmparray = importeddata.split("\n")
    for tmpline in tmparray:
      tmparr = tmpline.split(",")
      newdatetime = parse_date(tmparr[datetime_col], import_datetimeformat)
      amount = float(tmparr[amount_col])
      convertedvalue = amount*float(exrate)
      entity = transactions.add_transaction(db, newdatetime, amount, convertedvalue, tmparr[category_col], import_currency, tmparr[name_col], tmparr[description_col], acctid)
  except Exception as ex:
    result = str(ex)
  message(result)
  transactionlist = transactions.list_transactions(db, skip=0, limit=1000, filterby="", filtervalue="", sortby="")
  categorylist = weblists.get_weblist(db, "Category")
  currencylist = weblists.get_weblist(db, "Currency")
  accounttypelist = weblists.get_weblist(db, "AccountType")
  countrylist = weblists.get_weblist(db, "Country")
  accountlist = accounts.list_accounts(db, skip=0, limit=1000, filterby="", filtervalue="", sortby="")
  return templates.TemplateResponse("transactions.html", {"request": request, "messages": messages, "g": g, "categorylist": categorylist, "currencylist": currencylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "accountlist": accountlist, "transactionlist": transactionlist})

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