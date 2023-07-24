from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
app =FastAPI()

class Book(BaseModel):
    id: UUID
    title:str =  Field(min_length=1,max_length=50)
    author:str = Field(min_length=1,max_length=100)
    description: Optional[str] = Field(title="description of the book",
                            min_length=1,max_length=100)
    rating:int =Field(gt=-1,lt=101)

BOOKS =[]

@app.get("/")
async def read_all_books():
   if len(BOOKS) <1:
      create_books_no_api()
   return BOOKS

@app.post("/")
async def create_book(book:Book):
   BOOKS.append(book)
   return book

def create_books_no_api():
    book1=Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6",title="book1",author="author1",description="description1",rating=1)
    book2= Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="book2", author="author2", description="description2", rating=2)
    book3= Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="book3", author="author3", description="description3", rating=3)
    book4= Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="book4", author="author4", description="description4", rating=4)
    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)
