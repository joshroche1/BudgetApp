import os

from pydantic import BaseSettings
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schema


workingdir = os.getcwd()

class Settings(BaseSettings):
  app_name: str = "Budget App"
  database_vendor: str = ""
  database_host: str = ""
  database_port: str = ""
  database_name: str = ""
  database_user: str = ""
  database_password: str = ""
  ansible_config: str = ""
  ansible_hostsfile: str = ""
  ansible_basedir: str = ""
  ansible_playbookdir: str = ""
  base_dir: str = ""
  upload_dir: str = ""
  defaultcurrency: str = ""
  
  class Config:
    env_file = ".env"


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def get_weblist(db: Session, name: str):
  weblist = db.query(models.Weblist).filter(models.Weblist.name == name).all()
  return weblist

def add_weblist(db: Session, newname: str, newvalue: str):
  weblist = models.Weblist(name=newname, value=newvalue)
  db.add(weblist)
  db.commit()
  return weblist

def delete_weblist(db: Session, wlid):
  weblist = db.query(models.Weblist).filter(models.Weblist.id == wlid).first()
  if weblist is None:
    raise HTTPException(status_code=404, detail="Weblist not found")
  db.delete(weblist)
  db.commit()
  return True
