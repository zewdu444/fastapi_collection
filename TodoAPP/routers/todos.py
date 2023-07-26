import sys
sys.path.append('..')
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from .auth import get_current_user


router = APIRouter(prefix="/todos", tags=["todos"], responses={404: {"description": "Not found"}})

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

@router.get("/")
async def read_all(db: Session = Depends(get_db)):
  return  db.query(models.Todos).all()

@router.get("/user")
async def read_all(db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
   if current_user is None:
     raise HTTPException(status_code=401, detail="Not authenticated")
   return db.query(models.Todos).filter(models.Todos.owner_id == current_user.id).all()


@router.get("/{id}")
async def read_todo(id:int, db: Session = Depends(get_db), user:dict=Depends(get_current_user)):
  if user is None:
    raise HTTPException(status_code=401, detail="Not authenticated")
  todo_model = db.query(models.Todos).filter(models.Todos.id == id).filter(models.Todos.owner_id == user["id"]).first()
  if todo_model:
    return todo_model
  raise http_exception()

@router.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db), user:dict=Depends(get_current_user)):
  if user is None:
    raise HTTPException(status_code=401, detail="Not authenticated")
  todo_model = models.Todos(title=todo.title, description=todo.description, priority=todo.priority, complete=todo.complete, owner_id=user["id"])
  db.add(todo_model)
  db.commit()
  db.refresh(todo_model)
  return {"message": "Todo Created"}

@router.put("/{id}")
async def  update_todo(id:int, todo:Todo, db:Session=Depends(get_db), user:dict=Depends(get_current_user)):
       if user is None:
         raise HTTPException(status_code=401, detail="Not authenticated")
       todo_model= db.query(models.Todos).filter(models.Todos.id==id).filter(models.Todos.owner_id == user["id"]).first()
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

@router.delete("/{id}")

async def delete_todo(id:int, db:Session=Depends(get_db), user:dict =Depends(get_current_user)):
      todo_model=db.query(models.Todos).filter(models.Todos.id==id).filter(models.Todos.owner_id==user['id']).first()
      if todo_model is None:
        raise http_exception()
      db.query(models.Todos).filter(models.Todos.id==id).delete()
      db.commit()
      return {"message": "Todo Deleted"}


def http_exception():
  raise HTTPException(status_code=404, detail="Todo not found")

