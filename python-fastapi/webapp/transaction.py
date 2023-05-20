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

#