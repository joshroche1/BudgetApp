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
from . import models, schema, config, users, weblist
from .auth import authenticate_user, create_user, get_current_user, oauth2_scheme, get_users


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

app.include_router(users.router)
app.include_router(weblist.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
  message()
  return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "g": g})

@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
  settings = get_settings()
  return settings

@app.get("/test", response_class=HTMLResponse)
async def test(request: Request, db: Session = Depends(get_db)):
  message()
  settings = get_settings()
  userlist = get_users(db)
  return templates.TemplateResponse("test.html", {"request": request, "messages": messages, "g": g, "userlist": userlist, "settings": settings})

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
async def test(request: Request, db: Session = Depends(get_db)):
  message()
  settings = get_settings()
  userlist = get_users(db)
  weblistitems = await weblist.get_weblists(db)
  return templates.TemplateResponse("settings.html", {"request": request, "messages": messages, "g": g, "userlist": userlist, "settings": settings, "weblistitems": weblistitems})

##