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

