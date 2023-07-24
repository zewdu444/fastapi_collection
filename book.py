from fastapi import FastAPI
from enum import Enum
from typing import Optional
app = FastAPI()

BOOKS ={
   'book1':{
      'name':'The Great Gatsby',
      'author':'F. Scott Fitzgerald'
   },
   'book2':{
      'name':'The Da Vinci Code',
      'author':'Dan Brown'
   },
    'book3':{
        'name':'The Adventures of Sherlock Holmes',
        'author':'Sir Arthur Conan Doyle'
    },
    'book4':{
        'name':'the brief history of time',
        'author':'Stephen Hawking'
    },
     'book5':{
        'name':'The count of Monte Cristo',
        'author':'Alexandre Dumas'
     }
}

class DirectionName(str,Enum):
    east = "east"
    west = "west"
    north = "north"
    south = "south"


# read all books
@app.get("/")
async def read_all_boks(filter: Optional[str] = None):
   if filter:
       new_books =BOOKS.copy()
       del new_books[filter]
       return new_books
   return  BOOKS

# read only one book

@app.get("/{book_name}")
async def read_book(book_name:str):
   if book_name in BOOKS:
      return BOOKS[book_name]
   return {"Error":"Book not found"}




@app.get("/direction/{direction_name}")
async def get_direction(direction_name: DirectionName):
  if direction_name == DirectionName.north:
    return {"direction_name": direction_name, "message": "north direction"}
  if direction_name.value == "east":
    return {"direction_name": direction_name, "message": "east direction"}
  if  direction_name == DirectionName.west:
    return {"direction_name": direction_name, "message": "west direction"}
  if direction_name == DirectionName.south:
    return {"direction_name": direction_name, "message": "south direction"}

#  create new books
@app.post("/")
async  def create_book(book_name,book_author):
      if book_name in BOOKS:
         return {"Error":"Book already exists"}
      length = len(BOOKS)+1
      BOOKS[f"book{length}"] = {'name':book_name,'author':book_author}
      return BOOKS[f"book{length}"]

# update books
@app.put("/{book_name}")
async def update_book(book_name:str, name:str, book_author:str):
   if book_name in BOOKS:
      BOOKS[book_name] = {'name':name, 'author':book_author}
      return BOOKS[book_name]
   return {"Error":"Book not found"}


# delete book

@app.delete("/{book_name}")

async def delete_book(book_name:str):
   if book_name in BOOKS:
      del BOOKS[book_name]
      return {"Message":"Book deleted"}
   return {"Error":"Book not found"}
