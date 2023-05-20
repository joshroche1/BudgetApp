import os
import shutil
from typing import Union
from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schema, config
from .auth import authenticate_user, create_user, get_current_user, oauth2_scheme, get_users, get_user_by_username, update_user_email, update_user_password
from .filesystem import read_file, write_file, append_line, insert_line, delete_line
from .budget import get_budgets, get_budget, add_budget, delete_budget, update_budget_field
from .budgetitem import get_budgetitems, get_budgetitem, add_budgetitem, delete_budgetitem, update_budgetitem_field, get_budgetitems_for_budget
from .account import get_accounts, get_account, add_account, delete_account, update_account_field
from .transaction import get_transactions, get_transaction, add_transaction, delete_transaction, update_transaction_field

### Initialization

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

workingdir = os.getcwd()

messages = []
g = {}

@lru_cache
def get_settings():
  return config.Settings()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def message(message: str = ""):
  messages.clear()
  messages.append(message)

##
### Routing
##

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  message()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
  settings = get_settings()
  return settings

@app.get("/login", response_class=HTMLResponse)
async def loginpage(request: Request):
  message()
  return templates.TemplateResponse("login.html", {"request": request, "messages": messages, "g": g})

@app.post("/login")
async def loginform(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
  message()
  db_user = authenticate_user(db, username, password)
  if db_user is None:
    messages.append("User not found")
    return templates.TemplateResponse("login.html", {"request": request, "messages": messages, "g": g})
  g["user"] = db_user
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
  message()
  g.clear()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

## User Views

@app.get("/user", response_class=HTMLResponse)
async def userprofile(request: Request, db: Session = Depends(get_db)):
  message()
  user = get_user_by_username(db, g["user"]["username"])
  return templates.TemplateResponse("userprofile.html", {"request": request, "messages": messages, "g": g, "user": user})

@app.post("/user/update/email", response_class=HTMLResponse)
async def user_update_email(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
  message()
  user = get_user_by_username(db, g["user"]["username"])
  user = update_user_email(db, user.username, email)
  return templates.TemplateResponse("userprofile.html", {"request": request, "messages": messages, "g": g, "user": user})

@app.post("/user/update/password", response_class=HTMLResponse)
async def user_update_email(request: Request, password: str = Form(...), password2: str = Form(...), db: Session = Depends(get_db)):
  user = get_user_by_username(db, g["user"]["username"])
  if password != password2:
    message("Passwords must match")
  else:
    user = update_user_password(db, user.username, password)
  return templates.TemplateResponse("userprofile.html", {"request": request, "messages": messages, "g": g, "user": user})

##

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(get_db)):
  message()
  userlist = get_users(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  settings = get_settings()
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir})

@app.post("/category/create", response_class=HTMLResponse)
async def category_create(request: Request, category: str = Form(...), db: Session = Depends(get_db)):
  message()
  weblist = config.add_weblist(db, "Category", category)
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  userlist = get_users(db)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir})

@app.post("/category/delete/{id}", response_class=HTMLResponse)
async def category_delete(request: Request, id: int, db: Session = Depends(get_db)):
  message()
  if not config.delete_weblist(db, id):
    message("Error deleting category")
  userlist = get_users(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir})

## Budget Views

@app.get("/budget/overview", response_class=HTMLResponse)
async def budget_overview(request: Request, db: Session = Depends(get_db)):
  message()
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("overview.html", {"request": request, "messages": messages, "g": g, "categories": categories})

@app.get("/budget/list", response_class=HTMLResponse)
async def budget_list(request: Request, db: Session = Depends(get_db)):
  message()
  budgetlist = get_budgets(db)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("budget_list.html", {"request": request, "messages": messages, "g": g, "budgetlist": budgetlist, "categories": categories})

@app.get("/budget/detail/{id}", response_class=HTMLResponse)
async def budget_detail(request: Request, id: int, db: Session = Depends(get_db)):
  message()
  budget = get_budget(db, id)
  budgetitemlist = get_budgetitems_for_budget(db, id)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "budgetitemlist": budgetitemlist, "categories": categories})

@app.post("/budget/{id}/item/create", response_class=HTMLResponse)
async def budgetitem_create(request: Request, id: int, name: str = Form(...), description: str = Form(...), amount: str = Form(...), category: str = Form(...), recurrence: str = Form(...), recurrenceday: str = Form(...), db: Session = Depends(get_db)):
  message()
  newbudgetitem = {
    "name": name,
    "description": description,
    "amount": amount,
    "budgetid": id,
    "category": category,
    "recurrence": recurrence,
    "recurrenceday": recurrenceday
  }
  budget = get_budget(db, id)
  budgetitem = add_transaction(db, newbudgetitem)
  message(result)
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "budgetitem": budgetitem})

@app.post("/budget/{bid}/item/delete/{id}", response_class=HTMLResponse)
async def budgetitem_delete(request: Request, bid: int, id: int, db: Session = Depends(get_db)):
  budgetitem = get_budgetitem(db, id)
  if not delete_budgetitem(db, id):
    message("Error deleting transaction")
  message()
  budget = get_budget(db, id)
  budgetitemlist = get_budgetitems_for_budget(db, bid)
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budgetitemlist": budgetitemlist})

## Account Views

@app.get("/account/list", response_class=HTMLResponse)
async def account_list(request: Request, db: Session = Depends(get_db)):
  message()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("account_list.html", {"request": request, "messages": messages, "g": g, "accountlist": accountlist, "categories": categories, "currencylist": currencylist, "accounttypelist": accounttypelist})

@app.get("/account/detail/{id}", response_class=HTMLResponse)
async def account_detail(request: Request, id: int, db: Session = Depends(get_db)):
  message()
  account = get_account(db, id)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  countrylist = config.get_weblist(db, "Country")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("account_detail.html", {"request": request, "messages": messages, "g": g, "account": account, "categories": categories, "currencylist": currencylist, "countrylist": countrylist, "accounttypelist": accounttypelist})

@app.post("/account/create", response_class=HTMLResponse)
async def account_create(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
  message()
  newaccount = {
    "name": name,
    "accounttype": accounttype,
    "currency": currency,
    "iban": iban,
    "bic": bic,
    "country": country
  }
  account = add_account(db, newaccount)
  message(result)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  countrylist = config.get_weblist(db, "Country")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("account_detail.html", {"request": request, "messages": messages, "g": g, "account": account, "categories": categories, "currencylist": currencylist, "countrylist": countrylist, "accounttypelist": accounttypelist})

@app.post("/account/update/{id}/{field}", response_class=HTMLResponse)
async def account_update_field(request: Request, id: int, field: str, newvalue: str = Form(...), db: Session = Depends(get_db)):
  if update_account_field(db, id, field, newvalue):
    msg = "Updated [" + str(id) + "]: " + str(field) + " = " + str(newvalue)
  else:
    msg = "Could not update field"
  message(msg)
  account = get_account(db, id)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  countrylist = config.get_weblist(db, "Country")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("account_detail.html", {"request": request, "messages": messages, "g": g, "account": account, "categories": categories, "currencylist": currencylist, "countrylist": countrylist, "accounttypelist": accounttypelist})

@app.post("/account/delete/{id}", response_class=HTMLResponse)
async def account_delete(request: Request, id: int, db: Session = Depends(get_db)):
  account = get_account(db, id)
  if not delete_account(db, id):
    message("Error deleting account")
  message()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("account_list.html", {"request": request, "messages": messages, "g": g, "accountlist": accountlist, "categories": categories, "accounttypelist": accounttypelist})

## Transaction Views

@app.get("/transaction/list", response_class=HTMLResponse)
async def transaction_list(request: Request, db: Session = Depends(get_db)):
  message()
  transactionlist = get_transactions(db)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_list.html", {"request": request, "messages": messages, "g": g, "transactionlist": transactionlist, "categories": categories})

@app.get("/transaction/detail/{id}", response_class=HTMLResponse)
async def transaction_detail(request: Request, id: int, db: Session = Depends(get_db)):
  message()
  transaction = get_transaction(db, id)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_detail.html", {"request": request, "messages": messages, "g": g, "transaction": transaction, "categories": categories})
  
@app.post("/transaction/create", response_class=HTMLResponse)
async def transaction_create(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
  message()
  newtransaction = {
    "datetimestamp": datetimestamp,
    "amount": amount,
    "category": category,
    "name": name,
    "description": description,
    "accountid": accountid
  }
  transaction = add_transaction(db, newtransaction)
  categories = config.get_weblist(db, "Category")
  message(result)
  return templates.TemplateResponse("transaction_detail.html", {"request": request, "messages": messages, "g": g, "transaction": transaction, "categories": categories})

@app.post("/transaction/update/{id}/{field}", response_class=HTMLResponse)
async def transaction_update_field(request: Request, id: int, field: str, newvalue: str = Form(...), db: Session = Depends(get_db)):
  if update_transaction_field(db, id, field, newvalue):
    msg = "Updated [" + str(id) + "]: " + str(field) + " = " + str(newvalue)
  else:
    msg = "Could not update field"
  message(msg)
  transaction = get_transaction(db, id)
  return templates.TemplateResponse("transaction_detail.html", {"request": request, "messages": messages, "g": g, "transaction": transaction})

@app.post("/transaction/delete/{id}", response_class=HTMLResponse)
async def transaction_delete(request: Request, id: int, db: Session = Depends(get_db)):
  transaction = get_transaction(db, id)
  if not delete_transaction(db, id):
    message("Error deleting transaction")
  message()
  transactionlist = get_transactions(db)
  return templates.TemplateResponse("transaction_list.html", {"request": request, "messages": messages, "g": g, "transactionlist": transactionlist})

@app.get("/transaction/importview", response_class=HTMLResponse)
async def transaction_importview(request: Request, db: Session = Depends(get_db)):
  message()
  importdict = {}
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "importdict": importdict})

def parse_csv_info(csvfilecontent, delimiter):
  resultarr = []
  try:
    csvlines = csvfilecontent.splitlines()
    numcols = len(csvlines[0].split(delimiter))
    numrows = len(csvlines)
    for csvline in csvlines:
      csvitems = csvline.split(delimiter)
      tmplist = []
      for csvitem in csvitems:
        tmplist.append(csvitem)
      resultarr.append(tmplist)
    msg = "Colums: " + str(numcols) + " Rows: " + str(numrows)
    resultarr.append(msg)
  except Exception as ex:
    resultarr.append(str(ex))
  return resultarr

@app.post("/transaction/import", response_class=HTMLResponse)
async def transaction_import(request: Request, uploadedfile: UploadFile = File(...), fileformat: str = Form(...), header: str = Form(...), delimiter: str = Form(...), db: Session = Depends(get_db)):
  result = ""
  importdict = {}
  try:
    filename = uploadedfile.filename
    fileread = await uploadedfile.read()
    filecontents = str(fileread, 'iso-8859-1')
    importdict = parse_csv_info(filecontents, delimiter)
    result = "File: " + filename + "\nFile Format: " + fileformat + "\nFile Contents:\n" + filecontents
  except Exception as ex:
    result = str(ex)
  message(result)
  transactionlist = get_transactions(db)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "importdict": importdict})

###