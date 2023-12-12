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


def dates_parse_month(datestr: str):
  datearr = datestr.split("-")
  return datearr[1]

def dates_parse_year(datestr: str):
  datearr = datestr.split("-")
  return datearr[0]

def dates_month_list(startdate, enddate):
  nummonths = 0
  monthstart = 0
  montharr = []
  startdatearr = startdate.split("-")
  enddatearr = enddate.split("-")
  startyear = int(startdatearr[0])
  startmonth = int(startdatearr[1])
  startday = int(startdatearr[2])
  endyear = int(enddatearr[0])
  endmonth = int(enddatearr[1])
  endday = int(enddatearr[2])
  if startyear < endyear:
    if startmonth > endmonth:
      nummonths = (13 - startmonth) + endmonth
    elif startmonth < endmonth:
      nummonths = 13 + (endmonth - startmonth)
    else:
      nummonths = 12
  elif startyear == endyear:
    if startmonth == endmonth:
      nummonths = 1
    else:
      nummonths = (endmonth - startmonth) + 1
  else:
    nummonths = 12
  for monthno in range(nummonths-1):
    if (startmonth+monthno) > 12:
      montharr.append((startmonth+monthno)-12)
    else:
      montharr.append(startmonth+monthno)
  return montharr

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

def parse_overview_line_chart_data(transactionlist, budgetitemlist, startdate, enddate):
  resultdict = {}
  try:
    monthlist = dates_month_list(startdate, enddate)
    categorylist = ["Income"]
    for bitem in budgetitemlist:
      if categorylist.count(bitem.category) < 1:
        categorylist.append(bitem.category)
    for txaction in transactionlist:
      print(txaction)
      #
    #
  except Exception as ex:
    resultarr["Error"] = str(ex)
  return 0
