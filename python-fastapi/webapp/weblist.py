from fastapi import Depends, APIRouter

from sqlalchemy.orm import Session

from . import models, schema
from .database import SessionLocal


router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@router.get("/weblist/", tags=["weblist"])
async def get_weblists(db: Session = Depends(get_db)):
  weblists = db.query(models.Weblist).order_by(models.Weblist.name).all()
  return weblists

@router.get("/weblist/name/{name}", tags=["weblist"])
async def get_weblist(name: str, db: Session = Depends(get_db)):
  weblist = db.query(models.Weblist).filter(models.Weblist.name == name).all()
  return weblist

@router.get("/weblist/value/{value}", tags=["weblist"])
async def get_weblist_value(value: str, db: Session = Depends(get_db)):
  weblist = db.query(models.Weblist).filter(models.Weblist.value == value).first()
  return weblist

@router.post("/weblist/create", tags=["weblist"])
async def create_weblist(weblistname: str, weblistvalue: str, db: Session = Depends(get_db)):
  if not weblistname:
    return {"error":"Name needed"}
  if not weblistvalue:
    return {"error":"Value needed"}
  weblist = models.Weblist(name=weblistname, value=weblistvalue)
  db.add(weblist)
  db.commit()
  return weblist

@router.post("/weblist/delete/{value}", tags=["weblist"])
async def delete_weblist(value: str, db: Session = Depends(get_db)):
  weblist = db.query(models.Weblist).filter(models.Weblist.value == value).first()
  if weblist is None:
    raise HTTPException(status_code=404, detail="Weblist not found")
  db.delete(weblist)
  db.commit()
  return {"message":"Successfully delete weblist item"}
