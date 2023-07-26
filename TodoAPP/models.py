from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(100))
    priority = Column(Integer, default=1)
    complete= Column(Boolean, default=False)
