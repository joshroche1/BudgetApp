from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  username = Column(String, unique=True, index=True)
  password = Column(LargeBinary)


class Weblist(Base):
  __tablename__ = "weblist"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  value = Column(String)


class Budget(Base):
  __tablename__ = "budget"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  owner = Column(String)   # email address
  currency = Column(String)   # USD, EUR, ect...
  notes = Column(String)


class BudgetItem(Base):
  __tablename__ = "budgetitem"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  description = Column(String)
  amount = Column(String)
  budget = Column(Integer)   # Budget ID it is attached to
  itemtype = Column(String)   # Income, Bill, Expense, ect...
  category = Column(String)   # Paycheck, Pension, Mortgage, Rent, Utilities, Telecommunications, Entertainment, ect... 
  recurrence = Column(String)   # Daily, Weekly, Bi-weekly, Monthly, Quarterly, Bi-annually, Yearly, None
  recurrence_day = Column(Integer)   # day of month for recurrence, 1-31


class TransactionItem(Base):
  __tablename__ = "transactionitem"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  description = Column(String)
  amount = Column(String)
  itemtype = Column(String)   # Income, Bill, Expense, ect...
  category = Column(String)   # Paycheck, Pension, Mortgage, Rent, Utilities, Telecommunications, Entertainment, ect... 
  datetimestamp = Column(String)
  
