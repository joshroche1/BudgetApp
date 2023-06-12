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


def get_transactions(db: Session):
  transactionlist = db.query(models.Transaction).all()
  return transactionlist

def get_transactions_sorted(db: Session, field: str):
  if field == "id":
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.id)
  elif field == "name":
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.name)
  elif field == "amount":
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.amount)
  elif field == "datetimestamp":
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.datetimestamp.desc())
  elif field == "category":
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.category)
  elif field == "accountid":
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.accountid)
  else:
    transactionlist = db.query(models.Transaction).all()
  return transactionlist

def get_transactions_filtered(db: Session, field: str):
  #
  return 0

def get_transactions_dates(db: Session, startdate: str, enddate: str):
  transactionlist = db.query(models.Transaction).filter(models.Transaction.datetimestamp >= startdate).filter(models.Transaction.datetimestamp <= enddate).order_by(models.Transaction.datetimestamp.desc())
  return transactionlist

def get_transaction(db: Session, bid):
  transaction = db.query(models.Transaction).filter(models.Transaction.id == bid).first()
  return transaction

def add_transaction(db: Session, newtransaction):
  transaction = models.Transaction(name=newtransaction['name'], description=newtransaction['description'], amount=newtransaction['amount'], accountid=newtransaction['accountid'], category=newtransaction['category'], currency=newtransaction['currency'], datetimestamp=newtransaction['datetimestamp'])
  db.add(transaction)
  db.commit()
  return transaction

def delete_transaction(db: Session, bid):
  transaction = db.query(models.Transaction).filter(models.Transaction.id == bid).first()
  if transaction is None:
    raise HTTPException(status_code=404, detail="Transaction not found")
  db.delete(transaction)
  db.commit()
  return True

def update_transaction_field(db: Session, bid, field, newvalue):
  transaction = db.query(models.Transaction).filter(models.Transaction.id == bid).first()
  if field == "name": 
    transaction.name = newvalue
    db.commit()
  elif field == "description": 
    transaction.description = newvalue
    db.commit()
  elif field == "amount": 
    transaction.amount = newvalue
    db.commit()
  elif field == "accountid": 
    transaction.accountid = newvalue
    db.commit()
  elif field == "category": 
    transaction.category = newvalue
    db.commit()
  elif field == "datetimestamp": 
    transaction.datetimestamp = newvalue
    db.commit()
  else: 
    return False
  return True

def parse_csv_info(csvfilecontent, delimiter, filename, fileformat):
  resultarr = []
  try:
    csvlines = csvfilecontent.splitlines()
    numcols = len(csvlines[0].split(delimiter))
    numrows = len(csvlines)
    for csvline in csvlines:
      csvitems = csvline.split(delimiter)
      tmplist = []
      for csvitem in csvitems:
        tmpstr = csvitem.replace("\"","")
        tmplist.append(tmpstr)
      resultarr.append(tmplist)
  except Exception as ex:
    resultarr.append(str(ex))
  return resultarr

def parse_date(datetimestamp: str, dateformat: str):
  result = ""
  currentdate = datetime.now().strftime('%Y-%m-%d')
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
    print(result)
  except Exception as ex:
    print(str(ex))
    result = currentdate
  return result

def parse_format_csv(db: Session, csvfilecontent, delimiter, header, datetimefield, amountfield, categoryfield, namefield, descriptionfield, currency, accountid, dateformat):
  print(currency)
  resultarr = []
  try:
    csvlines = csvfilecontent.splitlines()
    numcols = len(csvlines[0].split(delimiter))
    numrows = len(csvlines)
    for csvline in csvlines:
      if header == "yes":
        resultarr.append("")
        header = "no"
      else:
        csvitems = csvline.split(delimiter)
        tmplist = []
        tmp1 = csvitems[int(datetimefield)-1].replace('"','')
        timestamp = parse_date(tmp1, dateformat)
        tmplist.append(timestamp)
        tmp2 = csvitems[int(amountfield)-1].replace('"','').replace(',','.')
        tmplist.append(tmp2)
        tmp3 = csvitems[int(categoryfield)-1].replace('"','')
        tmplist.append(tmp3)
        tmp4 = csvitems[int(namefield)-1].replace('"','')
        tmplist.append(tmp4)
        tmp5 = csvitems[int(descriptionfield)-1].replace('"','')
        tmplist.append(tmp5)
        resultarr.append(tmplist)
        newtransaction = {
          "datetimestamp": timestamp,
          "amount": float(tmp2),
          "category": tmp3,
          "name": tmp4,
          "description": tmp5,
          "currency": str(currency),
          "accountid": int(accountid)
        }
        add_transaction(db, newtransaction)
  except Exception as ex:
    resultarr.append(str(ex))
  return resultarr

def convert_value(db: Session, original, currency_from, currency_to):
  result = 0.0
  try:
    exrate = find_exchangerate(db, currency_from, currency_to)
    result = original * exrate
  except Exception as ex:
    print(str(ex))
    result = original
  return result

def get_table_data(db: Session, transactionlist, budgetcurrency):
  result = ""
  labels = ""
  amounts = ""
  try:
    resultdict = {}
    for transx in transactionlist:
      resultkeys = resultdict.keys()
      if transx.amount > 0: pass
      elif resultdict.get(transx.category, "None") != "None":
        if transx.currency is None:
          resultdict[transx.category] = resultdict[transx.category] + (transx.amount*(-1.0))
        elif transx.currency != budgetcurrency:
          tmpamt = convert_value(db, (transx.amount*(-1.0)), transx.currency, budgetcurrency)
          resultdict[transx.category] = resultdict[transx.category] + tmpamt
        else:
          resultdict[transx.category] = resultdict[transx.category] + (transx.amount*(-1.0))
      elif resultdict.get(transx.category, "None") == "None":
        if transx.currency is None:
          resultdict[transx.category] = resultdict[transx.category] + (transx.amount*(-1.0))
        elif transx.currency != budgetcurrency:
          tmpamt = convert_value(db, (transx.amount*(-1.0)), transx.currency, budgetcurrency)
          resultdict[transx.category] = tmpamt
        else:
          resultdict[transx.category] = (transx.amount*(-1.0))
    for newlabel in resultdict.keys():
      labels = labels + newlabel + ","
    for newvalue in resultdict.values():
      amounts = amounts + str(newvalue) + ","
    result = labels + "|" + amounts
  except Exception as ex:
    result = str(ex)
  return result

#