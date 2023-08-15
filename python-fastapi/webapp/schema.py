from typing import List, Union

from pydantic import BaseModel


class UserBase(BaseModel):
  email: str
  username: str

class UserCreate(UserBase):
  password: bytes

class User(UserBase):
  id: int

  class Config:
    orm_mode = True


class BudgetBase(BaseModel):
  name: str

class BudgetCreate(BudgetBase):
  description: str
  currency: str

class Budget(BudgetBase):
  id: int

  class Config:
    orm_mode = True


class BudgetItemBase(BaseModel):
  name: str
  amount: float

class BudgetItemCreate(BudgetItemBase):
  budgetid: int
  category: str
  recurrence: str
    

class BudgetItem(BudgetItemBase):
  id: int
  description: str
  recurrenceday: int

  class Config:
    orm_mode = True


class TransactionBase(BaseModel):
  datetimestamp: str
  amount: float
  convertedvalue: float
  name: str

class TransactionCreate(TransactionBase):
  description: str
  category: str
  accountid: int

class Transaction(TransactionBase):
  id: int
  currency: str

  class Config:
    orm_mode = True


class ExchangeRateBase(BaseModel):
  currency_from: str
  currency_ro: str

class ExchangeRateCreate(ExchangeRateBase):
  rate: float

class ExchangeRate(ExchangeRateBase):
  id: int

  class Config:
    orm_mode = True


class WeblistBase(BaseModel):
  name: str
  value: str

class WeblistCreate(WeblistBase):
  notes: str

class Weblist(WeblistBase):
  id: int

  class Config:
    orm_mode = True
