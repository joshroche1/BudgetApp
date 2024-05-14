from pydantic import BaseModel


class AccountBase(BaseModel):
  name: str
  description: str
  accounttype: str
  ownerid: int
  currency: str

class AccountCreate(AccountBase):
  pass

class Account(AccountBase):
  id: int
  
  class Config:
    orm_mode = True


class BudgetItemBase(BaseModel):
  name: str
  description: str
  amount: float
  category: str
  budgetid: int

class BudgetItemCreate(BudgetItemBase):
  pass
  
class BudgetItem(BudgetItemBase):
  id: int
  
  class Config:
    orm_mode = True


class BudgetBase(BaseModel):
  name: str
  description: str
  ownerid: int
  currency: str

class BudgetCreate(BudgetBase):
  pass
  
class Budget(BudgetBase):
  id: int
  budgetitems: list[BudgetItem] = []
  
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
  pass

class Weblist(WeblistBase):
  id: int

  class Config:
    orm_mode = True


class UserBase(BaseModel):
  email: str
  username: str

class UserCreate(UserBase):
  password: str

class User(UserBase):
  id: int
  budgets: list[Budget] = []
  accounts: list[Account] = []
  
  class Config:
    orm_mode = True


class TransactionBase(BaseModel):
  datetimestamp: str
  amount: float
  name: str
  description: str
  category: str
  currency: str
  accountid: int
  convertedvalue: float

class TransactionCreate(TransactionBase):
  pass

class Transaction(TransactionBase):
  id: int

  class Config:
    orm_mode = True
