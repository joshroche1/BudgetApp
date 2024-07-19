from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_weblists(db: Session):
  entitylist = db.query(models.Weblist).order_by(models.Weblist.id.asc()).all()
  return entitylist

def get_weblist(db: Session, name: str):
  entitylist = db.query(models.Weblist).filter(models.Weblist.name == name).order_by(models.Weblist.id.asc()).all()
  return entitylist

def add_weblist(db: Session, newname: str, newvalue: str):
  entity = models.Weblist(name=newname, value=newvalue)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_weblist(db: Session, id):
  entity = db.query(models.Weblist).filter(models.Weblist.id == id).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True
