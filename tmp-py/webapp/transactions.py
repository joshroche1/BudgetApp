from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas


def list_transactions(db: Session, skip: int = 0, limit: int = 1000, filterby: str = "", filtervalue: str = "", sortby: str = ""):
  if sortby == "name":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.name.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.name.asc()).offset(skip).limit(limit).all()
    elif filterby == "accountid": return db.query(models.Transaction).filter(models.Transaction.accountid == filtervalue).order_by(models.Transaction.name.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.name.asc()).offset(skip).limit(limit).all()
  elif sortby == "datetimestamp":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.datetimestamp.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.datetimestamp.asc().offset(skip).limit(limit)).all()
    elif filterby == "accountid": return db.query(models.Transaction).filter(models.Transaction.accountid == filtervalue).order_by(models.Transaction.datetimestamp.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.datetimestamp.asc()).offset(skip).limit(limit).all()
  elif sortby == "amount":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.amount.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.amount.asc()).offset(skip).limit(limit).all()
    elif filterby == "accountid": return db.query(models.Transaction).filter(models.Transaction.accountid == filtervalue).order_by(models.Transaction.amount.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.amount.asc()).offset(skip).limit(limit).all()
  elif sortby == "category":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.category.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.category.asc()).offset(skip).limit(limit).all()
    elif filterby == "accountid": return db.query(models.Transaction).filter(models.Transaction.accountid == filtervalue).order_by(models.Transaction.category.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.category.asc()).offset(skip).limit(limit).all()
  elif sortby == "currency":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.currency.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.currency.asc()).offset(skip).limit(limit).all()
    elif filterby == "accountid": return db.query(models.Transaction).filter(models.Transaction.accountid == filtervalue).order_by(models.Transaction.currency.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.currency.asc()).offset(skip).limit(limit).all()
  elif sortby == "accountid":
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.accountid.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.accountid.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.accountid.asc()).offset(skip).limit(limit).all()
  else:
    if filterby == "category": return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).order_by(models.Transaction.id.asc()).offset(skip).limit(limit).all()
    elif filterby == "currency": return db.query(models.Transaction).filter(models.Transaction.currency == filtervalue).order_by(models.Transaction.id.asc()).offset(skip).limit(limit).all()
    elif filterby == "accountid": return db.query(models.Transaction).filter(models.Transaction.accountid == filtervalue).order_by(models.Transaction.id.asc()).offset(skip).limit(limit).all()
    else: return db.query(models.Transaction).order_by(models.Transaction.id.asc()).offset(skip).limit(limit).all()

def list_transactions_by_dates(db: Session, startdate: str, enddate: str, filtervalue: str = ""):
  if filtervalue == "": return db.query(models.Transaction).filter(models.Transaction.datetimestamp >= startdate).filter(models.Transaction.datetimestamp <= enddate).order_by(models.Transaction.datetimestamp.desc()).all()
  return db.query(models.Transaction).filter(models.Transaction.category == filtervalue).filter(models.Transaction.datetimestamp >= startdate).filter(models.Transaction.datetimestamp <= enddate).order_by(models.Transaction.datetimestamp.desc()).all()

def get_transaction(db: Session, id):
  entity = db.query(models.Transaction).filter(models.Transaction.id == id).first()
  return entity

def create_transaction(db: Session, newtransaction):
  entity = models.Transaction(name=newtransaction.name, description=newtransaction.description, amount=newtransaction.amount, convertedvalue=newtransaction.convertedvalue, currency=newtransaction.currency, category=newtransaction.category, accountid=newtransaction.accountid, datetimestamp=newtransaction.datetimestamp)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def add_transaction(db: Session, newdatetimestamp, newamount, newconvertedvalue, newcategory, newcurrency, newname, newdescription, newaccountid):
  entity = models.Transaction(name=newname, description=newdescription, amount=newamount, convertedvalue=newconvertedvalue, currency=newcurrency, category=newcategory, accountid=newaccountid, datetimestamp=newdatetimestamp)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity

def update_transaction(db: Session, txaction: schemas.Transaction):
  entity = db.query(models.Transaction).filter(models.Transaction.id == txaction.id).first()
  entity = txaction
  db.persist(entity)
  db.commit()
  db.refresh(entity)
  return entity

def update_transaction_field(db: Session, id: int, fieldname: str, fieldvalue: str):
  entity = db.query(models.Transaction).filter(models.Transaction.id == id).first()
  if fieldname == "name": entity.name = fieldvalue
  elif fieldname == "description": entity.description = fieldvalue
  elif fieldname == "amount": entity.amount = fieldvalue
  elif fieldname == "convertedvalue": entity.convertedvalue = fieldvalue
  elif fieldname == "currency": entity.currency = fieldvalue
  elif fieldname == "category": entity.category = fieldvalue
  elif fieldname == "accountid": entity.accountid = fieldvalue
  elif fieldname == "datetimestamp": entity.datetimestamp = fieldvalue
  db.persist(entity)
  db.commit()
  db.refresh(entity)
  return entity

def delete_transaction(db: Session, bid):
  entity = db.query(models.Transaction).filter(models.Transaction.id == bid).first()
  if entity is None:
    return False
  db.delete(entity)
  db.commit()
  return True

def parse_overview_data(db: Session, startdate, enddate, budgetitemlist):
  txdict = {}
  montharr = []
  try:
    stdarr = startdate.split("-")
    endarr = enddate.split("-")
    styear = int(stdarr[0])
    stmonth = int(stdarr[1])
    endyear = int(endarr[0])
    endmonth = int(endarr[1])
    months = 0
    if styear < endyear:
      if stmonth >= endmonth:
        months = (12-endmonth) + stmonth
      elif stmonth < endmonth:
        months = endmonth - stmonth + 12
    elif styear == endyear:
      if stmonth < endmonth:
        months = endmonth - stmonth
      else:
        print("End month after start month: " + startdate + " " + enddate)
        return 0
    else:
      print("End date after start date: " + startdate + " " + enddate)
      return 0
    xLabels = []
    for bitem in budgetitemlist:
      if xLabels.count(bitem.category) >= 1:
        pass
      elif xLabels.count(bitem.category) < 1:
        xLabels.append(bitem.category)
    for i in range(months+1):
      if (int(stdarr[1])+i) > 12:
        if stmonth+i < 10:
          tmpstr = str(styear+1) + "-0" + str((stmonth+i)-12) + "-01"
          montharr.append(tmpstr)
        else:
          tmpstr = str(styear+1) + "-0" + str((stmonth+i)-12) + "-01"
          montharr.append(tmpstr)
      else:
        if stmonth+i < 10:
          tmpstr = str(styear) + "-0" + str(stmonth+i) + "-01"
          montharr.append(tmpstr)
        else:
          tmpstr = str(styear) + "-" + str(stmonth+i) + "-01"
          montharr.append(tmpstr)
    for xlabel in xLabels:
      tmpvalstr = ""
      for x in range(len(montharr)-1):
        tmpamt = 0.0
        txactions = list_transactions_by_dates(db,montharr[x],montharr[x+1],filtervalue=xlabel)
        for txaction in txactions:
          if xlabel == "Income":
            tmpamt = tmpamt + (txaction.convertedvalue*1.0)
          else:
            tmpamt = tmpamt + (txaction.convertedvalue*-1.0)
        tmpvalstr = tmpvalstr + str(tmpamt) + ","
      txdict[xlabel] = tmpvalstr
      txdict["Labels"] = xLabels
      txdict["Months"] = montharr
  except Exception as ex:
    txdict["error"] = str(ex)
  return txdict