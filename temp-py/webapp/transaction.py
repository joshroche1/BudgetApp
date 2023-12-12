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
  transactionlist = db.query(models.Transaction).order_by(models.Transaction.datetimestamp.desc()).all()
  return transactionlist

def get_transaction(db: Session, txid: int):
  transaction = db.query(models.Transaction).filter(models.Transaction.id == txid).first()
  return transaction

def add_transaction(db: Session, newtransaction):
  settings = config.Settings()
  amt = newtransaction['amount']
  cur=newtransaction['currency']
  if cur == settings.defaultcurrency:
    convertval = newtransaction['amount']
  else:
    convertval = convert_value(db, amt, cur, settings.defaultcurrency)
  transaction = models.Transaction(name=newtransaction['name'], description=newtransaction['description'], amount=amt, currency=cur, convertedvalue=convertval, accountid=newtransaction['accountid'], category=newtransaction['category'], datetimestamp=newtransaction['datetimestamp'])
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
  elif field == "convertedvalue": 
    transaction.convertedvalue = newvalue
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
#

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
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.datetimestamp.desc()).all()
  return transactionlist

def get_transactions_filtered(db: Session, field: str, value: str):
  if field == "name":
    svalue = "%" + value + "%"
    transactionlist = db.query(models.Transaction).filter(models.Transaction.name.match(svalue)).order_by(models.Transaction.datetimestamp.desc())
  elif field == "datetimestamp":
    svalue = "%" + value + "%"
    transactionlist = db.query(models.Transaction).filter(models.Transaction.datetimestamp.match(svalue)).order_by(models.Transaction.datetimestamp.desc())
  elif field == "category":
    transactionlist = db.query(models.Transaction).filter(models.Transaction.category == value).order_by(models.Transaction.datetimestamp.desc())
  elif field == "accountid":
    inval = int(value)
    transactionlist = db.query(models.Transaction).filter(models.Transaction.accountid == intval).order_by(models.Transaction.datetimestamp.desc())
  elif field == "currency":
    transactionlist = db.query(models.Transaction).filter(models.Transaction.currency == value).order_by(models.Transaction.datetimestamp.desc())
  else:
    transactionlist = db.query(models.Transaction).order_by(models.Transaction.datetimestamp.desc())
  return transactionlist

def get_transactions_dates(db: Session, startdate: str, enddate: str):
  transactionlist = db.query(models.Transaction).filter(models.Transaction.datetimestamp >= startdate).filter(models.Transaction.datetimestamp <= enddate).order_by(models.Transaction.datetimestamp.desc())
  return transactionlist

#
def import_csv_data(db: Session, csvcontent, delimiter, header, datetimefield, amountfield, categoryfield, namefield, descriptionfield, currency, accountid, dateformat):
  result = ""
  addedcount = 0
  try:
    csvlines = csvcontent.splitlines()
    for cline in csvlines:
      if header == "yes":
        continue
      else:
        citems = cline.split(delimiter)
        tmp1 = citems[int(datetimefield)-1].replace('"','')
        timestamp = parse_date(tmp1, dateformat)
        tmp2 = citems[int(amountfield)-1].replace('"','').replace(',','.')
        tmp3 = citems[int(categoryfield)-1].replace('"','')
        tmp4 = citems[int(namefield)-1].replace('"','')
        tmp5 = citems[int(descriptionfield)-1].replace('"','')
        msgout = "INSERT[transactions]: " + timestamp + " " + tmp3 + " " + tmp2 + " " + tmp4 + " " + tmp5
        print(msgout)
        newtransaction = {
          "datetimestamp": timestamp,
          "amount": float(tmp2),
          "category": tmp3,
          "name": tmp4,
          "description": tmp5,
          "currency": currency,
          "accountid": int(accountid)
        }
        added = add_transaction(db, newtransaction)
        if added != null:
          addedcount += 1
        else:
          print("Transaction not added")
    result = str(addedcount)
  except Exception as ex:
    result = str(ex)
  return result

def convert_value(db: Session, original, currency_from, currency_to):
  result = 0.0
  try:
    exrate = find_exchangerate(db, currency_from, currency_to)
    reslt = original * exrate
    result = float("{:.2f}".format(reslt))
  except Exception as ex:
    result = original
  return result

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
  except Exception as ex:
    print(str(ex))
    result = currentdate
  return result
#