from sqlalchemy import Column, Integer, String, Float, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True)
  email = Column(String, unique=True)
  password = Column(LargeBinary)
  budgets = relationship("Budget", back_populates="owner")
  accounts = relationship("Account", back_populates="owner")


class Budget(Base):
  __tablename__ = "budgets"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, default="")
  description = Column(String, default="")
  currency = Column(String, default="")
  ownerid = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", back_populates="budgets")
  budgetitems = relationship("BudgetItem", back_populates="owner")


class BudgetItem(Base):
  __tablename__ = "budgetitems"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, default="")
  description = Column(String, default="")
  amount = Column(Float)
  budgetid = Column(Integer, ForeignKey("budgets.id"))
  owner = relationship("Budget", back_populates="budgetitems")


class Account(Base):
  __tablename__ = "accounts"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, default="")
  description = Column(String, default="")
  currency = Column(String, default="")
  ownerid = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", back_populates="accounts")


class Transaction(Base):
  __tablename__ = "transactions"
  id = Column(Integer, primary_key=True, index=True)
  datetimestamp = Column(String)
  amount = Column(Float)
  convertedvalue = Column(Float)
  category = Column(String, default="")
  currency = Column(String, default="")
  name = Column(String, default="")
  description = Column(String, default="")
  accountid = Column(Integer, ForeignKey("accounts.id"))
