import json
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .exchangerate import find_exchangerate
from . import models, schema, config


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


def parse_csv_data(csvcontent, delimiter):
  resultarr = []
  try:
    csvlines = csvcontent.splitlines()
    numcols = len(csvlines[0].split(delimiter))
    numrows = len(csvlines)
    for cline in csvlines:
      citems = cline.split(delimiter)
      tmplist = []
      for citem in citems:
        tmpstr = citem.replace("\"","").replace(",",".")
        tmplist.append(tmpstr)
      resultarr.append(tmplist)
  except Exception as ex:
    resultarr.append(str(ex))
  return resultarr
