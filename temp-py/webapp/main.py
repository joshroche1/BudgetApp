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
from .budgetitem import get_budgetitems, get_budgetitem, add_budgetitem, delete_budgetitem, update_budgetitem_field
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

#######
## REST
#######

@app.get("/account/")
async def get_account_all(request: Request, db: Session = Depends(get_db)):
  accounts = get_accounts(db)
  return accounts

@app.get("/account/{acctid}")
async def get_account(request: Request, acctid: int, db: Session = Depends(get_db)):
  account = db.query(models.Account).filter(models.Account.id == acctid).first()
  if account is None:
    raise HTTPException(status_code=404, detail="Account not found")
  jsondata = jsonable_encoder(account)
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
