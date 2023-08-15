import os
import shutil
import json
from typing import Union
from functools import lru_cache
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schema, config
from .auth import authenticate_user, create_user, get_current_user, oauth2_scheme, get_users, get_user_by_username, update_user_email, update_user_password
from .filesystem import read_file, write_file, append_line, insert_line, delete_line, upload_file, get_uploaded_files, delete_file, get_ical_file
from .budget import get_budgets, get_budget, add_budget, delete_budget, update_budget_field
from .budgetitem import get_budgetitems, get_budgetitem, add_budgetitem, delete_budgetitem, update_budgetitem_field, get_budgetitems_for_budget, get_budget_data
from .account import get_accounts, get_account, add_account, delete_account, update_account_field
from .transaction import get_transactions, get_transactions_sorted, get_transaction, add_transaction, delete_transaction, update_transaction_field, parse_csv_info, parse_format_csv,get_transactions_dates, get_table_data, get_category_data, get_transactions_filtered
from .exchangerate import get_exchangerates, get_exchangerate, add_exchangerate, delete_exchangerate, update_exchangerate_field

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

##########
## Routing
##########

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  message()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
  settings = get_settings()
  return settings

@app.get("/testdata")
async def info(request: Request):
  testarr = "Price Size,50 4,48 2,42 3,55 5,58 6,59 1,52 3,51 2,61 7,60 8"
  return testarr

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

#######
## User
#######

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

###########
## Settings
###########

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(get_db)):
  message()
  userlist = get_users(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  exhangeratelist = get_exchangerates(db)
  settings = get_settings()
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir, "exhangeratelist": exhangeratelist})

@app.post("/category/create", response_class=HTMLResponse)
async def category_create(request: Request, category: str = Form(...), db: Session = Depends(get_db)):
  message()
  weblist = config.add_weblist(db, "Category", category)
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  exhangeratelist = get_exchangerates(db)
  settings = get_settings()
  userlist = get_users(db)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir, "exhangeratelist": exhangeratelist})

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
  exhangeratelist = get_exchangerates(db)
  settings = get_settings()
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir, "exhangeratelist": exhangeratelist})

@app.post("/exchangerate/create", response_class=HTMLResponse)
async def exchangerate_create(request: Request, currency_from: str = Form(...), currency_to: str = Form(...), rate: str = Form(...), db: Session = Depends(get_db)):
  message()
  newexchangerate = {
    "currency_from": currency_from,
    "currency_to": currency_to,
    "rate": rate
  }
  exchangerate = add_exchangerate(db, newexchangerate)
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  exhangeratelist = get_exchangerates(db)
  settings = get_settings()
  userlist = get_users(db)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir, "exhangeratelist": exhangeratelist})

@app.post("/exchangerate/delete/{id}", response_class=HTMLResponse)
async def exchangerate_delete(request: Request, id: int, db: Session = Depends(get_db)):
  message()
  if not delete_exchangerate(db, id):
    message("Error deleting ExhangeRate")
  userlist = get_users(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  exhangeratelist = get_exchangerates(db)
  settings = get_settings()
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categories": categories, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir, "exhangeratelist": exhangeratelist})

#########
## Budget
#########

@app.get("/budget/overview", response_class=HTMLResponse)
async def budget_overview(request: Request, db: Session = Depends(get_db)):
  message()
  currentdate = datetime.now()
  month = str(currentdate.month-1)
  if len(month) < 2: month = "0" + month
  startdate = str(currentdate.year) + "-" + month + "-01"
  enddate = str(currentdate.year) + "-" + month + "-32"
  transactionlist = get_transactions_dates(db, startdate, enddate)
  budget = get_budget(db, 1)
  budgetlist = get_budgets(db)
  budgetidlist = []
  for budget in budgetlist:
    budgetidlist.append(budget.id)
  budgetitemlist = get_budgetitems_for_budget(db, 1)
  budgetsum = 0.00
  budgetremain = 0.00
  for budgetitem in budgetitemlist:
    if budgetitem.category == "Income":
      budgetremain = budgetremain + budgetitem.amount
    else:
      budgetremain = budgetremain - budgetitem.amount
      budgetsum = budgetsum + budgetitem.amount
  tabledata = get_table_data(db, transactionlist, budget.currency)
  budgettabledata = get_budget_data(budgetitemlist)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("overview.html", {"request": request, "messages": messages, "g": g, "categories": categories, "transactionlist": transactionlist, "tabledata": tabledata, "budgetidlist": budgetidlist,"budget": budget, "budgetitemlist": budgetitemlist, "budgetsum": budgetsum, "budgetremain": budgetremain, "budgettabledata": budgettabledata})

@app.post("/budget/overview/filtered/month", response_class=HTMLResponse)
async def budget_overview_month(request: Request, month: str = Form(...), db: Session = Depends(get_db)):
  message()
  currentdate = datetime.now()
  startdate = str(currentdate.year) + "-" + month + "-01"
  enddate = str(currentdate.year) + "-" + month + "-32"
  transactionlist = get_transactions_dates(db, startdate, enddate)
  budget = get_budget(db, 1)
  budgetlist = get_budgets(db)
  budgetidlist = []
  for budget in budgetlist:
    budgetidlist.append(budget.id)
  budgetitemlist = get_budgetitems_for_budget(db, 1)
  budgetsum = 0.00
  budgetremain = 0.00
  for budgetitem in budgetitemlist:
    if budgetitem.category == "Income":
      budgetremain = budgetremain + budgetitem.amount
    else:
      budgetremain = budgetremain - budgetitem.amount
      budgetsum = budgetsum + budgetitem.amount
  tabledata = get_table_data(db, transactionlist, budget.currency)
  budgettabledata = get_budget_data(budgetitemlist)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("overview.html", {"request": request, "messages": messages, "g": g, "categories": categories, "transactionlist": transactionlist, "tabledata": tabledata, "budgetidlist": budgetidlist,"budget": budget, "budgetitemlist": budgetitemlist, "budgetsum": budgetsum, "budgetremain": budgetremain, "budgettabledata": budgettabledata})

@app.get("/budget/list", response_class=HTMLResponse)
async def budget_list(request: Request, db: Session = Depends(get_db)):
  message()
  budgetlist = get_budgets(db)
  currencylist = config.get_weblist(db, "Currency")
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("budget_list.html", {"request": request, "messages": messages, "g": g, "budgetlist": budgetlist, "categories": categories})

@app.get("/budget/detail/{id}", response_class=HTMLResponse)
async def budget_detail(request: Request, id: int, db: Session = Depends(get_db)):
  message()
  budget = get_budget(db, id)
  budgetitemlist = get_budgetitems_for_budget(db, id)
  budgetsum = 0.00
  budgetincome = 0.00
  budgetexpense = 0.00
  for budgetitem in budgetitemlist:
    if budgetitem.category == "Income":
      budgetsum = budgetsum + budgetitem.amount
      budgetincome += budgetitem.amount
    else:
      budgetsum = budgetsum - budgetitem.amount
      budgetexpense += budgetitem.amount
  currencylist = config.get_weblist(db, "Currency")
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "budgetitemlist": budgetitemlist, "categories": categories, "budgetsum": budgetsum, "budgetincome": budgetincome, "budgetexpense": budgetexpense})

#############
## BudgetItem
#############

@app.get("/budgetitem/detail/{id}", response_class=HTMLResponse)
async def budgetitem_detail(request: Request, id: int, db: Session = Depends(get_db)):
  message()
  currentdate = datetime.now()
  startdate = str(currentdate.year-1) + "-" + str(currentdate.month) + str(currentdate.day)
  enddate = str(currentdate.year) + "-" + str(currentdate.month) + str(currentdate.day)
  budgetitem = get_budgetitem(db, id)
  categories = config.get_weblist(db, "Category")
  transactionlist = get_transactions_filtered(db, "category", budgetitem.category)
  budgetitemdata = get_category_data(db, budgetitem.category, startdate, enddate)
  return templates.TemplateResponse("budgetitem_detail.html", {"request": request, "messages": messages, "g": g, "budgetitem": budgetitem, "categories": categories, "budgetitemdata": budgetitemdata, "transactionlist": transactionlist})

@app.post("/budgetitem/create", response_class=HTMLResponse)
async def budgetitem_create(request: Request, budgetid: str = Form(...), name: str = Form(...), description: str = Form(...), amount: str = Form(...), category: str = Form(...), recurrence: str = Form(...), recurrenceday: str = Form(...), db: Session = Depends(get_db)):
  message()
  newbudgetitem = {
    "name": name,
    "description": description,
    "amount": amount,
    "budgetid": budgetid,
    "category": category,
    "recurrence": recurrence,
    "recurrenceday": recurrenceday
  }
  budgetitem = add_budgetitem(db, newbudgetitem)
  message("Created Budget Item: " + name)
  currentdate = datetime.now()
  startdate = str(currentdate.year-1) + "-" + str(currentdate.month) + str(currentdate.day)
  enddate = str(currentdate.year) + "-" + str(currentdate.month) + str(currentdate.day)
  budgetitem = get_budgetitem(db, budgetid)
  categories = config.get_weblist(db, "Category")
  transactionlist = get_transactions_filtered(db, "category", budgetitem.category)
  budgetitemdata = get_category_data(db, budgetitem.category, startdate, enddate)
  return templates.TemplateResponse("budgetitem_detail.html", {"request": request, "messages": messages, "g": g, "budgetitem": budgetitem, "categories": categories, "budgetitemdata": budgetitemdata, "transactionlist": transactionlist})

@app.post("/budgetitem/update/{id}/{field}", response_class=HTMLResponse)
async def budgetitem_update(request: Request, id: int, field: str, value: str = Form(...), db: Session = Depends(get_db)):
  message()
  if not update_budgetitem_field(db, id, field, value):
    message("Error updating " + field)
  else:
    message("Updated " + field + " to " + str(value))
  currentdate = datetime.now()
  startdate = str(currentdate.year-1) + "-" + str(currentdate.month) + str(currentdate.day)
  enddate = str(currentdate.year) + "-" + str(currentdate.month) + str(currentdate.day)
  budgetitem = get_budgetitem(db, id)
  categories = config.get_weblist(db, "Category")
  transactionlist = get_transactions_filtered(db, "category", budgetitem.category)
  budgetitemdata = get_category_data(db, budgetitem.category, startdate, enddate)
  return templates.TemplateResponse("budgetitem_detail.html", {"request": request, "messages": messages, "g": g, "budgetitem": budgetitem, "categories": categories, "budgetitemdata": budgetitemdata, "transactionlist": transactionlist})

@app.post("/budgetitem/delete/{id}", response_class=HTMLResponse)
async def budgetitem_delete(request: Request, id: int, db: Session = Depends(get_db)):
  budgetitem = get_budgetitem(db, id)
  bid = budgetitem.budgetid
  if not delete_budgetitem(db, id):
    message("Error deleting transaction")
  else:
    message("Deleted Budget Item: " + str(id))
  budget = get_budget(db, bid)
  budgetitemlist = get_budgetitems_for_budget(db, bid)
  currencylist = config.get_weblist(db, "Currency")
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budgetitemlist": budgetitemlist, "budget": budget})

@app.get("/budgetitem/{id}/ical", response_class=HTMLResponse)
async def budgetitem_get_ical(request: Request, bid: int, id: int, db: Session = Depends(get_db)):
  budgetitem = get_budgetitem(db, id)
  icalfile = get_ical_file(budgetitem.recurrenceday, budgetitem.amount, budgetitem.name)
  budget = get_budget(db, bid)
  budgetitemlist = get_budgetitems_for_budget(db, bid)
  budgetsum = 0.00
  for budgetitem in budgetitemlist:
    if budgetitem.category == "Income":
      budgetsum = budgetsum + budgetitem.amount
    else:
      budgetsum = budgetsum - budgetitem.amount
  currencylist = config.get_weblist(db, "Currency")
  categories = config.get_weblist(db, "Category")
  file_name = str(budgetitem.name).lower() + ".ical"
  return FileResponse(icalfile, media_type='application/octet-stream', filename=file_name)

##########
## Account
##########

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
async def account_create(request: Request, name: str = Form(...), accounttype: str = Form(...), currency: str = Form(...), iban: str = Form(...), bic: str = Form(...), country: str = Form(...), db: Session = Depends(get_db)):
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
  message(account)
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

##############
## Transaction
##############

@app.get("/transaction/list", response_class=HTMLResponse)
async def transaction_list(request: Request, db: Session = Depends(get_db)):
  message()
  transactionlist = get_transactions(db)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_list.html", {"request": request, "messages": messages, "g": g, "transactionlist": transactionlist, "categories": categories})

@app.get("/transaction/list/sorted/{field}", response_class=HTMLResponse)
async def transaction_list_sorted(request: Request, field: str, db: Session = Depends(get_db)):
  message()
  transactionlist = get_transactions_sorted(db, field)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_list.html", {"request": request, "messages": messages, "g": g, "transactionlist": transactionlist, "categories": categories})

@app.post("/transaction/list/filtered/category", response_class=HTMLResponse)
async def transaction_list_categoryfilter(request: Request, filtervalue: str = Form(...), db: Session = Depends(get_db)):
  message()
  transactionlist = get_transactions_filtered(db, "Categiry", filtervalue)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_list.html", {"request": request, "messages": messages, "g": g, "transactionlist": transactionlist, "categories": categories})

@app.post("/transaction/list/filtered/date", response_class=HTMLResponse)
async def transaction_list_datefilter(request: Request, startdate: str = Form(...), enddate: str = Form(...), db: Session = Depends(get_db)):
  message()
  transactionlist = get_transactions_dates(db, startdate, enddate)
  categories = config.get_weblist(db, "Category")
  return templates.TemplateResponse("transaction_list.html", {"request": request, "messages": messages, "g": g, "transactionlist": transactionlist, "categories": categories})

@app.post("/transaction/list/filtered/month", response_class=HTMLResponse)
async def transaction_list_monthfilter(request: Request, month: str = Form(...), db: Session = Depends(get_db)):
  message()
  currentdate = datetime.now()
  startdate = str(currentdate.year) + "-" + month + "-01"
  enddate = str(currentdate.year) + "-" + month + "-32"
  transactionlist = get_transactions_dates(db, startdate, enddate)
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
  uploadedfilelist = get_uploaded_files()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "currencylist": currencylist, "accountlist": accountlist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

@app.post("/uploads/{file}", response_class=HTMLResponse)
async def uploads_deletefile(request: Request, file: str, db: Session = Depends(get_db)):
  result = delete_file("uploads/" + file)
  importdict = {}
  message(result)
  uploadedfilelist = get_uploaded_files()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "currencylist": currencylist, "accountlist": accountlist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

"""
Import writes file into upload folder.
MAKE SELECTION BOX FOR FILE TO PARSE INTO TRANSACTIONS WITH FORMAT

"""
@app.post("/transaction/import", response_class=HTMLResponse)
async def transaction_import(request: Request, uploadedfile: UploadFile = File(...), fileformat: str = Form(...), header: str = Form(...), delimiter: str = Form(...), db: Session = Depends(get_db)):
  result = ""
  importdict = {}
  try:
    filename = uploadedfile.filename
    fileread = await uploadedfile.read()
    filecontents = str(fileread, 'iso-8859-1')
    upload_result = upload_file(filename, filecontents)
    message(upload_result)
    importdict = parse_csv_info(filecontents, delimiter, filename, fileformat)
    result = "File: " + filename + "\nFile Format: " + fileformat + "\nFile Contents:\n" + filecontents
  except Exception as ex:
    result = str(ex)
  message(result)
  uploadedfilelist = get_uploaded_files()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "currencylist": currencylist, "accountlist": accountlist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

@app.post("/transaction/uploadedfileview", response_class=HTMLResponse)
async def transaction_uploadedfileview(request: Request, uploadedfile: str = Form(...), db: Session = Depends(get_db)):
  result = ""
  importdict = {}
  try:
    filepath = "/upload/" + uploadedfile
    filecontents = read_file(filepath)
    result = "File: " + uploadedfile + "\nFile Contents:\n" + filecontents
  except Exception as ex:
    result = str(ex)
  message(result)
  uploadedfilelist = get_uploaded_files()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "currencylist": currencylist, "accountlist": accountlist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

@app.post("/transaction/uploadedformatview", response_class=HTMLResponse)
async def transaction_uploadedformatview(request: Request, uploadedfile: str = Form(...), delimiter: str = Form(...), fileformat: str = Form(...), db: Session = Depends(get_db)):
  result = ""
  importdict = {}
  try:
    filepath = "/upload/" + uploadedfile
    filecontents = read_file(filepath)
    importdict = parse_csv_info(filecontents, delimiter, uploadedfile, fileformat)
    result = "File: " + uploadedfile
  except Exception as ex:
    result = str(ex)
  message(result)
  uploadedfilelist = get_uploaded_files()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "currencylist": currencylist, "accountlist": accountlist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

@app.post("/transaction/importformatted", response_class=HTMLResponse)
async def transaction_importformatted(request: Request, uploadedfile: str = Form(...), delimiter: str = Form(...), currency: str = Form(...), header: str = Form(...), accountid: str = Form(...), datetimefield: str = Form(...), amountfield: str = Form(...), categoryfield: str = Form(...), namefield: str = Form(...), descriptionfield: str = Form(...), dateformat: str = Form(...), country: str = Form(...), db: Session = Depends(get_db)):
  result = ""
  importdict = {}
  try:
    filepath = "/upload/" + uploadedfile
    filecontents = read_file(filepath)
    result = parse_format_csv(db, filecontents, delimiter, header, datetimefield, amountfield, categoryfield, namefield, descriptionfield, currency, accountid, dateformat, country)
  except Exception as ex:
    result = str(ex)
  message(result)
  uploadedfilelist = get_uploaded_files()
  accountlist = get_accounts(db)
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  importdict = {}
  return templates.TemplateResponse("transaction_import.html", {"request": request, "messages": messages, "g": g, "categories": categories, "currencylist": currencylist, "accountlist": accountlist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

############
############
