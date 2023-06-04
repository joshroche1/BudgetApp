from fastapi import HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
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

def get_transaction(db: Session, bid):
  transaction = db.query(models.Transaction).filter(models.Transaction.id == bid).first()
  return transaction

def add_transaction(db: Session, newtransaction):
  transaction = models.Transaction(name=newtransaction['name'], description=newtransaction['description'], amount=newtransaction['amount'], accountid=newtransaction['accountid'], category=newtransaction['category'], datetimestamp=newtransaction['datetimestamp'])
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

def parse_format_csv(db: Session, csvfilecontent, delimiter, header, datetimefield, amountfield, categoryfield, namefield, descriptionfield, currency, accountid):
  print("parse_format_csv")
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
        tmplist.append(tmp1)
        print(tmp1)
        tmp2 = csvitems[int(amountfield)-1].replace('"','').replace(',','.')
        tmplist.append(tmp2)
        print(tmp2)
        tmp3 = csvitems[int(categoryfield)-1].replace('"','')
        tmplist.append(tmp3)
        print(tmp3)
        tmp4 = csvitems[int(namefield)-1].replace('"','')
        tmplist.append(tmp4)
        print(tmp4)
        tmp5 = csvitems[int(descriptionfield)-1].replace('"','')
        tmplist.append(tmp5)
        print(tmp5)
        resultarr.append(tmplist)
        newtransaction = {
          "datetimestamp": tmp1,
          "amount": float(tmp2),
          "category": tmp3,
          "name": tmp4,
          "description": tmp5,
          "currency": currency,
          "accountid": int(accountid)
        }
        add_transaction(db, newtransaction)
  except Exception as ex:
    resultarr.append(str(ex))
  return resultarr

#