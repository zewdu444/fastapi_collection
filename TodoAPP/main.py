from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

class Todo(BaseModel):
  title: str = Field(..., example="Buy Milk")
  description: Optional[str] = Field(..., example="Go to the store and buy milk")
  priority: int = Field(..., example=1, gt=0, lt=6)
  complete: bool = Field(..., example=False)

@app.get("/")
async def read_all(db: Session = Depends(get_db)):
  return  db.query(models.Todos).all()

@app.get("/{id}")

async def read_todo(id:int, db: Session = Depends(get_db)):
  todo_model = db.query(models.Todos).filter(models.Todos.id == id).first()
  if todo_model:
    return todo_model
  raise http_exception()

@app.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
  todo_model = models.Todos(title=todo.title, description=todo.description, priority=todo.priority, complete=todo.complete)
  db.add(todo_model)
  db.commit()
  db.refresh(todo_model)
  return {"message": "Todo Created"}

@app.put("/{id}")
async def  update_todo(id:int, todo:Todo, db:Session=Depends(get_db)):
       todo_model= db.query(models.Todos).filter(models.Todos.id==id).first()
       if todo_model is None:
         raise http_exception()
       todo_model.title=todo.title
       todo_model.description=todo.description
       todo_model.priority=todo.priority
       todo_model.complete=todo.complete
       db.add(todo_model)
       db.commit()
       db.refresh(todo_model)
       return {"message": "Todo Updated"}
def http_exception():
  raise HTTPException(status_code=404, detail="Todo not found")
