from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True, index=True)
      username = Column(String(50), unique=True, index=True)
      email = Column(String(100), unique=True, index=True)
      first_name = Column(String)
      last_name = Column(String)
      hashed_password = Column(String)
      is_active = Column(Boolean, default=True)
      todos = relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(100))
    priority = Column(Integer, default=1)
    complete= Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="todos")
