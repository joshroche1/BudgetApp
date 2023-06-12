from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  username = Column(String, unique=True, index=True)
  password = Column(LargeBinary)

class Account(Base):
  __tablename__ = "accounts"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  accounttype = Column(String, default="")
  currency = Column(String, default="")
  iban = Column(String, default="")
  bic = Column(String, default="")
  country = Column(String, default="")

class Budget(Base):
  __tablename__ = "budgets"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  currency = Column(String)
  description = Column(String, default="")

class BudgetItem(Base):
  __tablename__ = "budgetitems"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  description = Column(String, default="")
  amount = Column(Float)
  budgetid = Column(Integer)
  category = Column(String, default="")
  recurrence = Column(String, default="")
  recurrenceday = Column(Integer)
  
class Transaction(Base):
  __tablename__ = "transactions"
  
  id = Column(Integer, primary_key=True, index=True)
  datetimestamp = Column(String)
  amount = Column(Float)
  category = Column(String, default="")
  currency = Column(String, default="")
  name = Column(String, default="")
  description = Column(String, default="")
  accountid = Column(Integer)

class ExchangeRate(Base):
  __tablename__ = "exchangerate"
  
  id = Column(Integer, primary_key=True, index=True)
  currency_from = Column(String, default="")
  currency_to = Column(String, default="")
  rate = Column(Float)

class Weblist(Base):
  __tablename__ = "weblist"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  value = Column(String)

