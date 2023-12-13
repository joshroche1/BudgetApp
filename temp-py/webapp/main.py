import os
import shutil
import json
from typing import Union
from functools import lru_cache
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, File, Form, Request, UploadFile
from fastapi.encoders import jsonable_encoder
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
from .budgetitem import get_budgetitems, get_budgetitem, add_budgetitem, delete_budgetitem, update_budgetitem_field, get_budgetitems_by_budget, get_budget_data
from .exchangerate import get_exchangerates, get_exchangerate, find_exchangerate, add_exchangerate, delete_exchangerate, update_exchangerate_field
from .account import get_accounts, get_account, add_account, delete_account, update_account_field
from .transaction import get_transactions, get_transaction, add_transaction, delete_transaction, update_transaction_field, get_transactions_dates, import_csv_data, get_line_chart_data, get_pie_chart_data
from .datautility import parse_csv_data, dates_month_list

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
  messages.clear()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
  settings = get_settings()
  return settings

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
  messages.clear()
  return templates.TemplateResponse("login.html", {"request": request, "messages": messages, "g": g})

@app.post("/login")
async def loginform(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
  messages.clear()
  db_user = authenticate_user(db, username, password)
  if db_user is None:
    messages.append("User not found")
    return templates.TemplateResponse("login.html", {"request": request, "messages": messages, "g": g})
  g["user"] = db_user
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
  messages.clear()
  g.clear()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(get_db)):
  messages.clear()
  userlist = get_users(db)
  categorylist = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  exchangeratelist = get_exchangerates(db)
  settings = get_settings()
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "categorylist": categorylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "userlist": userlist, "settings": settings, "workingdir": workingdir, "exchangeratelist": exchangeratelist})

@app.get("/overview/filter", response_class=HTMLResponse)
async def overview_filtered(request: Request, budgetid: int | None = None, month: int | None = None, startdate: str | None = None, enddate: str | None = None, db: Session = Depends(get_db)):
  messages.clear()
  monthlist = [1,2,3,4,5,6,7,8,9,10,11,12]
  if startdate is not None:
    if enddate is not None:
      monthlist = dates_month_list(startdate, enddate)
  if budgetid is None:
    budgetid = 1
  budget = db.query(models.Budget).filter(models.Budget.id == budgetid).first()
  xLabels = ""
  for month in range(len(monthlist)):
    xLabels += str(month) + ","
  budgetitems = get_budgetitems_by_budget(db, budgetid)
  accountlist = get_accounts(db)
  budgetlist = get_budgets(db)
  transactions = get_transactions_dates(db, startdate, enddate)
  categorylist = config.get_weblist(db, "Category")
  txlabels = []
  for category in categorylist:
    txlabels.append(category.value)
  txdict = get_line_chart_data(db, txlabels, startdate, enddate)
  piedata = get_pie_chart_data(db, transactions, budget.currency, txlabels)
  pielabels = ""
  pieamounts = ""
  lablarr = piedata.keys()
  for labl in lablarr:
    if piedata[labl] is not None:
      pielabels = pielabels + labl + ","
      pieamounts = pieamounts + str(piedata[labl]) + ","
  piechartdata = pielabels + "|" + pieamounts
  budgetitemdata = get_budget_data(budgetitems)
  bilabels = ""
  biamounts = ""
  for bilabel in budgetitemdata.keys():
    bilabels = bilabels + bilabel + ","
  for value in budgetitemdata.values():
    biamounts = biamounts + str(value) + ","
  budgetchartdata = bilabels + "|" + biamounts
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  return templates.TemplateResponse("overview.html", {"request": request, "messages": messages, "g": g, "budget": budget, "budgetitems": budgetitems, "accountlist": accountlist, "budgetlist": budgetlist, "transactions": transactions, "txdict": txdict, "xLabels": xLabels, "piechartdata": piechartdata, "piedata": piedata, "budgetchartdata": budgetchartdata, "categorylist": categorylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist})

@app.get("/overview/{bid}", response_class=HTMLResponse)
async def overview(request: Request, bid: int, db: Session = Depends(get_db)):
  messages.clear()
  currentdate = datetime.now()
  startdate = str(currentdate.year - 1) + "-" + str(currentdate.month) + "-" + str(currentdate.day)
  enddate = str(currentdate.year) + "-" + str(currentdate.month) + "-" + str(currentdate.day)
  xLabels = ""
  for i in range(12):
    if (currentdate.month+i) > 12:
      xLabels = xLabels + str(currentdate.year) + "-" + str((currentdate.month+i)-12) + ","
    else:
      xLabels = xLabels + str(currentdate.year - 1) + "-" + str(currentdate.month+i) + ","
  budget = db.query(models.Budget).filter(models.Budget.id == bid).first()
  budgetitems = get_budgetitems_by_budget(db, bid)
  accountlist = get_accounts(db)
  budgetlist = get_budgets(db)
  transactions = get_transactions_dates(db, startdate, enddate)
  categorylist = config.get_weblist(db, "Category")
  txlabels = []
  for category in categorylist:
    txlabels.append(category.value)
  txdict = get_line_chart_data(db, txlabels, startdate, enddate)
  piedata = get_pie_chart_data(db, transactions, budget.currency, txlabels)
  pielabels = ""
  pieamounts = ""
  lablarr = piedata.keys()
  for labl in lablarr:
    if piedata[labl] is not None:
      pielabels = pielabels + labl + ","
      pieamounts = pieamounts + str(piedata[labl]) + ","
  piechartdata = pielabels + "|" + pieamounts
  budgetitemdata = get_budget_data(budgetitems)
  bilabels = ""
  biamounts = ""
  for bilabel in budgetitemdata.keys():
    bilabels = bilabels + bilabel + ","
  for value in budgetitemdata.values():
    biamounts = biamounts + str(value) + ","
  budgetchartdata = bilabels + "|" + biamounts
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  return templates.TemplateResponse("overview.html", {"request": request, "messages": messages, "g": g, "budget": budget, "budgetitems": budgetitems, "accountlist": accountlist, "budgetlist": budgetlist, "transactions": transactions, "txdict": txdict, "xLabels": xLabels, "piechartdata": piechartdata, "piedata": piedata, "budgetchartdata": budgetchartdata, "categorylist": categorylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist})

@app.get("/budgetview/{bid}", response_class=HTMLResponse)
async def budget_view(request: Request, bid: int, db: Session = Depends(get_db)):
  messages.clear()
  budget = db.query(models.Budget).filter(models.Budget.id == bid).first()
  budgetlist = get_budgets(db)
  budgetitems = get_budgetitems_by_budget(db, bid)
  categorylist = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  return templates.TemplateResponse("budget.html", {"request": request, "messages": messages, "g": g, "budget": budget, "budgetlist": budgetlist, "budgetitems": budgetitems, "categorylist": categorylist, "currencylist": currencylist})

@app.get("/accountview/{acctid}", response_class=HTMLResponse)
async def account_view(request: Request, acctid: int, db: Session = Depends(get_db)):
  messages.clear()
  account = db.query(models.Account).filter(models.Account.id == acctid).first()
  accountlist = get_accounts(db)
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  currencylist = config.get_weblist(db, "Currency")
  return templates.TemplateResponse("account.html", {"request": request, "messages": messages, "g": g, "account": account, "accountlist": accountlist, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist})

@app.get("/transactionsview", response_class=HTMLResponse)
async def transactions_view(request: Request, db: Session = Depends(get_db)):
  messages.clear()
  accountlist = get_accounts(db)
  budgetlist = get_budgets(db)
  transactions = get_transactions(db)
  categorylist = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  return templates.TemplateResponse("transactions.html", {"request": request, "messages": messages, "g": g, "accountlist": accountlist, "budgetlist": budgetlist, "transactions": transactions, "categorylist": categorylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist})

@app.get("/importcsvdata", response_class=HTMLResponse)
async def importcsv_view(request: Request, db: Session = Depends(get_db)):
  messages.clear()
  importdict = {}
  accountlist = get_accounts(db)
  budgetlist = get_budgets(db)
  uploadedfilelist = get_uploaded_files()
  categorylist = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  return templates.TemplateResponse("importcsv.html", {"request": request, "messages": messages, "g": g, "accountlist": accountlist, "budgetlist": budgetlist, "categorylist": categorylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

@app.post("/uploadfile", response_class=HTMLResponse)
async def upload_file_view(request: Request, uploadedfile: UploadFile = File(...), fileformat: str = Form(...), header: str = Form(...), delimiter: str = Form(...), db: Session = Depends(get_db)):
  result = ""
  importdict = {}
  try:
    filename = uploadedfile.filename
    fileread = await uploadedfile.read()
    filecontents = str(fileread, 'iso-8859-1')
    upload_result = upload_file(filename, filecontents)
    importdict = parse_csv_data(filecontents, delimiter)
    result = upload_result
  except Exception as ex:
    result = str(ex)
  message(result)
  accountlist = get_accounts(db)
  uploadedfilelist = get_uploaded_files()
  categories = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  return templates.TemplateResponse("importcsv.html", {"request": request, "messages": messages, "g": g, "categories": categories, "currencylist": currencylist, "accountlist": accountlist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

@app.post("/transaction/importdata", response_class=HTMLResponse)
async def transaction_importdata(request: Request, uploadedfile: str = Form(...), delimiter: str = Form(...), currency: str = Form(...), header: str = Form(...), accountid: str = Form(...), datetimefield: str = Form(...), amountfield: str = Form(...), categoryfield: str = Form(...), namefield: str = Form(...), descriptionfield: str = Form(...), dateformat: str = Form(...), country: str = Form(...), db: Session = Depends(get_db)):
  result = ""
  importdict = {}
  try:
    filepath = "/upload/" + uploadedfile
    filecontents = read_file(filepath)
    result = import_csv_data(db, filecontents, delimiter, header, datetimefield, amountfield, categoryfield, namefield, descriptionfield, currency, accountid, dateformat)
  except Exception as ex:
    result = str(ex)
  message(result)
  importdict = {}
  budgetlist = get_budgets(db)
  accountlist = get_accounts(db)
  uploadedfilelist = get_uploaded_files()
  categorylist = config.get_weblist(db, "Category")
  currencylist = config.get_weblist(db, "Currency")
  accounttypelist = config.get_weblist(db, "AccountType")
  countrylist = config.get_weblist(db, "Country")
  return templates.TemplateResponse("importcsv.html", {"request": request, "messages": messages, "g": g, "accountlist": accountlist, "budgetlist": budgetlist, "categorylist": categorylist, "accounttypelist": accounttypelist, "countrylist": countrylist, "currencylist": currencylist, "importdict": importdict, "uploadedfilelist": uploadedfilelist})

#######
## REST
#######

@app.get("/account/")
async def get_account_all(request: Request, db: Session = Depends(get_db)):
  accounts = get_accounts(db)
  jsondata = jsonable_encoder(accounts)
  return jsondata

@app.get("/account/{acctid}")
async def get_account(request: Request, acctid: int, db: Session = Depends(get_db)):
  account = db.query(models.Account).filter(models.Account.id == acctid).first()
  if account is None:
    raise HTTPException(status_code=404, detail="Account not found")
  jsondata = jsonable_encoder(account)
  return jsondata

@app.get("/budget/")
async def get_budget_all(request: Request, db: Session = Depends(get_db)):
  budgets = get_budgets(db)
  jsondata = jsonable_encoder(budgets)
  return jsondata

@app.get("/budget/{bid}")
async def get_budget(request: Request, bid: int, db: Session = Depends(get_db)):
  budget = db.query(models.Budget).filter(models.Budget.id == bid).first()
  if budget is None:
    raise HTTPException(status_code=404, detail="Budget not found")
  jsondata = jsonable_encoder(budget)
  return jsondata

@app.get("/budgetitem/")
async def get_budgetitem_all(request: Request, db: Session = Depends(get_db)):
  budgetitems = get_budgetitems(db)
  jsondata = jsonable_encoder(budgetitems)
  return jsondata

@app.get("/budgetitem/{biid}")
async def get_budgetitem(request: Request, biid: int, db: Session = Depends(get_db)):
  budgetitem = db.query(models.BudgetItem).filter(models.BudgetItem.id == biid).first()
  if budgetitem is None:
    raise HTTPException(status_code=404, detail="BudgetItem not found")
  jsondata = jsonable_encoder(budgetitem)
  return jsondata

@app.get("/transaction/")
async def get_transaction_all(request: Request, db: Session = Depends(get_db)):
  transactions = get_transactions(db)
  jsondata = jsonable_encoder(transactions)
  return jsondata

@app.get("/transaction/{txid}")
async def get_transaction(request: Request, txid: int, db: Session = Depends(get_db)):
  transaction = db.query(models.Transaction).filter(models.Transaction.id == txid).first()
  if transaction is None:
    raise HTTPException(status_code=404, detail="Transaction not found")
  jsondata = jsonable_encoder(transaction)
  return jsondata

############
############
