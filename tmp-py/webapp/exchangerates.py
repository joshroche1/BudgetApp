from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_exchangerates(db: Session):
  entitylist = db.query(models.ExchangeRate).order_by(models.ExchangeRate.id.asc()).all()
  return entitylist

def get_exchangerate(db: Session, id: int):
  entity = db.query(models.ExchangeRate).filter(models.ExchangeRate.id == id).first()
  return entity

def get_exchangerate_from_to(db: Session, ex_from: str, ex_to: str):
  try:
    entity = db.query(models.ExchangeRate).filter(models.ExchangeRate.currency_from == ex_from).filter(models.ExchangeRate.currency_to == ex_to).first()
  except Exception as ex:
    return {"error": str(ex)}
  return entity

def add_exchangerate(db: Session, new_from: str, new_to: str, newrate: float):
  entity = models.ExchangeRate(currency_from=new_from, currency_to=new_to, rate=newrate)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_exchangerate(db: Session, id: int):
  entity = db.query(models.ExchangeRate).filter(models.ExchangeRate.id == id).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True
