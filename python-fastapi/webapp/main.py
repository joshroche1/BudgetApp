import os
import shutil
import datetime
from typing import Union
from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schema, config, users, weblist
from .auth import authenticate_user, create_user, get_current_user, oauth2_scheme, get_users
from .budget import get_budget, get_budgets, create_budget, delete_budget
from .budgetitem import get_budgetitems, get_budgetitem, get_items_for_budget, create_budgetitem, delete_budgetitem, get_items_for_budget_by_type


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

##
##
### Routing
##
##

#app.include_router(users.router)
#app.include_router(weblist.router)
#app.include_router(budget.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  message()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/login", response_class=HTMLResponse)
async def loginpage(request: Request):
  message()
  return templates.TemplateResponse("login.html", {"request": request, "messages": messages, "g": g})

@app.post("/login")
async def loginform(request: Request, username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
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

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request, db: Session = Depends(get_db)):
  message()
  settings = get_settings()
  userlist = get_users(db)
  weblistitems = await weblist.get_weblists(db)
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "userlist": userlist, "settings": settings, "weblistitems": weblistitems})


## Budget Views ##


@app.get("/budget/", tags=["budget"])
async def view_budget(request: Request, db: Session = Depends(get_db)):
  budgets = await get_budgets(db)
  budgetitemdict = {}
  for bdgt in budgets:
    budgetitems = await get_items_for_budget(bdgt.id, db)
    budgetitemdict[bdgt.id] = budgetitems
  wl_currency = await weblist.get_weblist("Currency", db)
  message()
  return templates.TemplateResponse("budget.html", {"request": request, "messages": messages, "g": g, "budgets": budgets, "budgetitemdict": budgetitemdict, "wl_currency": wl_currency})


@app.get("/budget/detail/{id}", tags=["budget"])
async def view_budget_detail(id: int, request: Request, db: Session = Depends(get_db)):
  budget = await get_budget(id, db)
  incomeitems = await get_items_for_budget_by_type(id, "Income", db)
  expenseitems = await get_items_for_budget_by_type(id, "Expense", db)
  wl_type = await weblist.get_weblist("Type", db)
  wl_category = await weblist.get_weblist("Category", db)
  wl_recurrence = await weblist.get_weblist("Recurrence", db)
  message()
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "incomeitems": incomeitems, "expenseitems": expenseitems, "wl_type": wl_type, "wl_category": wl_category, "wl_recurrence": wl_recurrence})


@app.post("/budget/detail/{id}/updatevalues", tags=["budget"])
async def view_budget_detail_update_values(id: int, request: Request, db: Session = Depends(get_db)):
  result = ""
  try:
    budget = await get_budget(id, db)
    incomeitems = await get_items_for_budget_by_type(id, "Income", db)
    expenseitems = await get_items_for_budget_by_type(id, "Expense", db)
    incomeamount = 0.0
    expenseamount = 0.0
    for incitem in incomeitems:
      tmpflt = float(incitem.amount)
      incomeamount = incomeamount + tmpflt
    for expitem in expenseitems:
      tmpflt = float(expitem.amount)
      expenseamount = expenseamount + tmpflt
    budget.incometotal = incomeamount
    budget.expensetotal = expenseamount
    tmprem = incomeamount - expenseamount
    budget.remainder = tmprem
    db.commit()
  except Exception as ex:
    result = str(ex)
  updatedbudget = await get_budget(id, db)
  incomeitems = await get_items_for_budget_by_type(id, "Income", db)
  expenseitems = await get_items_for_budget_by_type(id, "Expense", db)
  wl_type = await weblist.get_weblist("Type", db)
  wl_category = await weblist.get_weblist("Category", db)
  wl_recurrence = await weblist.get_weblist("Recurrence", db)
  message(result)
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": updatedbudget, "incomeitems": incomeitems, "expenseitems": expenseitems, "wl_type": wl_type, "wl_category": wl_category, "wl_recurrence": wl_recurrence})


@app.post("/budget/create", tags=["budget"])
async def view_budget_create(request: Request, name: str = Form(), owner: str = Form(), currency: str = Form(), notes: str = Form(), db: Session = Depends(get_db)):
  try:
    budget = await create_budget(name, owner, currency, notes, db)
    incomeitems = await get_items_for_budget_by_type(budget.id, "Income", db)
    expenseitems = await get_items_for_budget_by_type(budget.id, "Expense", db)
    wl_type = await weblist.get_weblist("Type", db)
    wl_category = await weblist.get_weblist("Category", db)
    wl_recurrence = await weblist.get_weblist("Recurrence", db)
    message()
    return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "incomeitems": incomeitems, "expenseitems": expenseitems, "wl_type": wl_type, "wl_category": wl_category, "wl_recurrence": wl_recurrence})
  except Exception as ex:
    message(str(ex))
    budgets = await get_budgets(db)
    budgetitemdict = {}
    for bdgt in budgets:
      budgetitems = await get_items_for_budget(bdgt.id, db)
      budgetitemdict[bdgt.id] = budgetitems
    wl_currency = await weblist.get_weblist("Currency", db)
    return templates.TemplateResponse("budget.html", {"request": request, "messages": messages, "g": g, "budgets": budgets, "budgetitemdict": budgetitemdict, "wl_currency": wl_currency})


@app.post("/budget/delete/{bid}", tags=["budget"])
async def view_budget_delete(request: Request, bid: int, db: Session = Depends(get_db)):
  try:
    budget = await delete_budget(bid, db)
  except Exception as ex:
    message(str(ex))
    budgets = await get_budgets(db)
    budgetitemdict = {}
    for bdgt in budgets:
      budgetitems = await get_items_for_budget(bdgt.id, db)
      budgetitemdict[bdgt.id] = budgetitems
    wl_currency = await weblist.get_weblist("Currency", db)
    return templates.TemplateResponse("budget.html", {"request": request, "messages": messages, "g": g, "budgets": budgets, "budgetitemdict": budgetitemdict, "wl_currency": wl_currency})
  budgets = await get_budgets(db)
  budgetitemdict = {}
  for bdgt in budgets:
    budgetitems = await get_items_for_budget(bdgt.id, db)
    budgetitemdict[bdgt.id] = budgetitems
  wl_currency = await weblist.get_weblist("Currency", db)
  message()
  return templates.TemplateResponse("budget.html", {"request": request, "messages": messages, "g": g, "budgets": budgets, "budgetitemdict": budgetitemdict, "wl_currency": wl_currency})


@app.post("/budgetitem/create", tags=["budgetitem"])
async def view_budgetitem_create(request: Request, name: str = Form(), amount: str = Form(), budgetid: int = Form(), itemtype: str = Form(), category: str = Form(), recurrence: str = Form(), recurrence_day: int = Form(), db: Session = Depends(get_db)):
  try:
    budgetitem = await create_budgetitem(name, amount, budgetid, itemtype, category, recurrence, recurrence_day, db)
    budget = await get_budget(budgetid, db)
    incomeitems = await get_items_for_budget_by_type(budgetid, "Income", db)
    expenseitems = await get_items_for_budget_by_type(budgetid, "Expense", db)
    wl_type = await weblist.get_weblist("Type", db)
    wl_category = await weblist.get_weblist("Category", db)
    wl_recurrence = await weblist.get_weblist("Recurrence", db)
    message()
    return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "incomeitems": incomeitems, "expenseitems": expenseitems, "wl_type": wl_type, "wl_category": wl_category, "wl_recurrence": wl_recurrence})
  except Exception as ex:
    message(str(ex))
    budget = await get_budget(budgetid, db)
    incomeitems = await get_items_for_budget_by_type(budgetid, "Income", db)
    expenseitems = await get_items_for_budget_by_type(budgetid, "Expense", db)
    wl_type = await weblist.get_weblist("Type", db)
    wl_category = await weblist.get_weblist("Category", db)
    wl_recurrence = await weblist.get_weblist("Recurrence", db)
    return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "incomeitems": incomeitems, "expenseitems": expenseitems, "wl_type": wl_type, "wl_category": wl_category, "wl_recurrence": wl_recurrence})


@app.post("/budgetitem/delete/{biid}", tags=["budgetitem"])
async def view_budgetitem_delete(request: Request, biid: int, budgetid: int = Form(), db: Session = Depends(get_db)):
  try:
    budgetitem = await delete_budgetitem(biid, db)
  except Exception as ex:
    message(str(ex))
    budget = await get_budget(budgetid, db)
    incomeitems = await get_items_for_budget_by_type(budgetid, "Income", db)
    expenseitems = await get_items_for_budget_by_type(budgetid, "Expense", db)
    wl_type = await weblist.get_weblist("Type", db)
    wl_category = await weblist.get_weblist("Category", db)
    wl_recurrence = await weblist.get_weblist("Recurrence", db)
    return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "incomeitems": incomeitems, "expenseitems": expenseitems, "wl_type": wl_type, "wl_category": wl_category, "wl_recurrence": wl_recurrence})
  budget = await get_budget(budgetid, db)
  incomeitems = await get_items_for_budget_by_type(budgetid, "Income", db)
  expenseitems = await get_items_for_budget_by_type(budgetid, "Expense", db)
  wl_type = await weblist.get_weblist("Type", db)
  wl_category = await weblist.get_weblist("Category", db)
  wl_recurrence = await weblist.get_weblist("Recurrence", db)
  message()
  return templates.TemplateResponse("budget_detail.html", {"request": request, "messages": messages, "g": g, "budget": budget, "incomeitems": incomeitems, "expenseitems": expenseitems, "wl_type": wl_type, "wl_category": wl_category, "wl_recurrence": wl_recurrence})

@app.get("/budgetitem/ical/{biid}", tags=["budgetitem"])
async def get_budgetitem_ical(request: Request, biid: int, db: Session = Depends(get_db)):
  budgetitem = await get_budgetitem(biid, db)
  budget = await get_budget(biid, db)
  currenttime = datetime.datetime.now()
  currenttimestamp = currenttime.strftime("%Y%m%d%H%M%S%Z")
  dtstamp = currenttime.strftime("%Y%m")
  if budgetitem.recurrence_day < 10: 
    dtstamp = dtstamp + "0" + str(budgetitem.recurrence_day) + ""
  else:
    dtstamp = dtstamp + str(budgetitem.recurrence_day) + ""
  filecontents = "BEGIN:VCALENDAR\n"
  filecontents = filecontents + "VERSION:2.0\n"
  filecontents = filecontents + "PRODID:-//" + budgetitem.name + "\n"
  filecontents = filecontents + "BEGIN:VEVENT\n"
  filecontents = filecontents + "UID:" + currenttimestamp + "\n"
  filecontents = filecontents + "TRANSP:TRANSPARENT\n"
  filecontents = filecontents + "DTSTART:" + dtstamp + "\n"
  filecontents = filecontents + "DTEND:" + dtstamp + "\n"
  filecontents = filecontents + "DTSTAMP:" + dtstamp + "\n"
  filecontents = filecontents + "ORGANIZER;CN=:mailto:" + budget.owner + "\n"
  filecontents = filecontents + "SUMMARY:" + budgetitem.amount + "\n"
  filecontents = filecontents + "DESCRIPTION:" + budgetitem.category + "\n"
  filecontents = filecontents + "LOCATION:\n"
  filecontents = filecontents + "END:VEVENT\n"
  filecontents = filecontents + "END:VCALENDAR\n"
  tmpfilename = "/tmp/tmp_ical_" + currenttimestamp + ".ical"
  icalfile = open(tmpfilename,"w")
  icalfile.write(filecontents)
  icalfile.close()
  return FileResponse(tmpfilename, media_type="calendar")
