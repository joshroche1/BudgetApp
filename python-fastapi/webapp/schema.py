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
