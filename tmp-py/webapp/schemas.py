from pydantic import BaseModel


class AccountBase(BaseModel):
  name: str
  description: str
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
