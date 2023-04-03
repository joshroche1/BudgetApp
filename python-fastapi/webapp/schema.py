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


class WeblistBase(BaseModel):
  name: str
  value: str

class WeblistCreate(WeblistBase):
  notes: str

class Weblist(WeblistBase):
  id: int

  class Config:
    orm_mode = True


class BudgetBase(BaseModel):
  name: str
  owner: str
  currency: str

class BudgetCreate(BudgetBase):
  notes: str

class Budget(BudgetBase):
  id: int

  class Config:
    orm_mode = True


class BudgetItemBase(BaseModel):
  name: str
  amount: str
  budget: int
  itemtype: str
  category: str
  recurrence: str
  recurrence_day: str

class BudgetItemCreate(BudgetItemBase):
  description: str

class BudgetItem(BudgetItemBase):
  id: int

  class Config:
    orm_mode = True


class TransactionItemBase(BaseModel):
  name: str
  amount: str
  datetimestamp: str
  itemtype: str
  category: str

class TransactionItemCreate(TransactionItemBase):
  description: str

class TransactionItem(BudgetItemBase):
  id: int

  class Config:
    orm_mode = True