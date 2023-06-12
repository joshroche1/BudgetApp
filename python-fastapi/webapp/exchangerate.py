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


def get_exchangerates(db: Session):
  exchangeratelist = db.query(models.ExchangeRate).all()
  return exchangeratelist

def get_exchangerate(db: Session, bid):
  exchangerate = db.query(models.ExchangeRate).filter(models.ExchangeRate.id == bid).first()
  return exchangerate

def find_exchangerate(db: Session, cur_from, cur_to):
  print(cur_from)
  print(cur_to)
  result = 1.0
  try:
    exchangerate = db.query(models.ExchangeRate).filter(models.ExchangeRate.currency_from == cur_from, models.ExchangeRate.currency_to == cur_to).first()
    result = exchangerate.rate
  except Exception as ex:
    print(str(ex))
  return result

def add_exchangerate(db: Session, newexchangerate):
  exchangerate = models.ExchangeRate(currency_from=newexchangerate['currency_from'], currency_to=newexchangerate['currency_to'], rate=newexchangerate['rate'])
  db.add(exchangerate)
  db.commit()
  return exchangerate

def delete_exchangerate(db: Session, bid):
  exchangerate = db.query(models.ExchangeRate).filter(models.ExchangeRate.id == bid).first()
  if exchangerate is None:
    raise HTTPException(status_code=404, detail="ExchangeRate not found")
  db.delete(exchangerate)
  db.commit()
  return True

def update_exchangerate_field(db: Session, bid, field, newvalue):
  exchangerate = db.query(models.ExchangeRate).filter(models.ExchangeRate.id == bid).first()
  if field == "currency_from": 
    exchangerate.currency_from = newvalue
    db.commit()
  elif field == "currency_to": 
    exchangerate.currency_to = newvalue
    db.commit()
  elif field == "rate": 
    exchangerate.rate = newvalue
    db.commit()
  else: 
    return False
  return True

#