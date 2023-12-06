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


def get_accounts(db: Session):
  accountlist = db.query(models.Account).all()
  return accountlist

def get_account(db: Session, acctid):
  account = db.query(models.Account).filter(models.Account.id == acctid).first()
  return account

def add_account(db: Session, newaccount):
  account = models.Account(name=newaccount['name'], accounttype=newaccount['accounttype'], currency=newaccount['currency'],  country=newaccount['country'])
  db.add(account)
  db.commit()
  return account

def delete_account(db: Session, acctid):
  account = db.query(models.Account).filter(models.Account.id == acctid).first()
  if account is None:
    raise HTTPException(status_code=404, detail="Account not found")
  db.delete(account)
  db.commit()
  return True

def update_account_field(db: Session, acctid, field, newvalue):
  account = db.query(models.Account).filter(models.Account.id == acctid).first()
  if field == "name": 
    account.name = newvalue
    db.commit()
  elif field == "accounttype": 
    account.accounttype = newvalue
    db.commit()
  elif field == "currency": 
    account.currency = newvalue
    db.commit()
  elif field == "country": 
    account.country = newvalue
    db.commit()
  else: 
    return False
  return True

#