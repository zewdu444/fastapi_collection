from fastapi import FastAPI, HTTPException,Request, status, Form, Header
from pydantic import BaseModel,Field
from typing import Optional, Annotated
from uuid import UUID
from starlette.responses import JSONResponse

class NegativeNumberException(Exception):
      def __init__(self, books_to_return):
         self.books_to_return =books_to_return

app =FastAPI()

class Book(BaseModel):
    id: UUID
    title:str =  Field(min_length=1,max_length=50)
    author:str = Field(min_length=1,max_length=100)
    description: Optional[str] = Field(title="description of the book",
                            min_length=1,max_length=100)
    rating:int =Field(gt=-1,lt=101)

    model_config={
       "json_schema_extra" : {
           "examples":[
              {
              "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
               "title": "tilayen kedemkut",
               "author": "tilaye",
               "description": "biography of tilaye",
               "rating": 20
              }
          ]
    }
       }

class BookNoRating(BaseModel):
    id: UUID
    title:str =  Field(min_length=1,max_length=50)
    author :str = Field(min_length=1,max_length=100)
    description: Optional[str] = Field(title="description of the book",
                            min_length=1,max_length=100)

BOOKS =[]

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=400,
        content={"message": f"Negative number {exception.books_to_return} is invalid"},
    )


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
   if books_to_return and books_to_return < 0:
      raise NegativeNumberException(books_to_return)
   if len(BOOKS) <1:
      create_books_no_api()
   if books_to_return and len(BOOKS) >= books_to_return >0:
       return BOOKS[:books_to_return]
   return BOOKS

@app.get("/no_rating", response_model= list [BookNoRating])
async def read_all_books(books_to_return: Optional[int] = None):
   if books_to_return and books_to_return < 0:
      raise NegativeNumberException(books_to_return)
   if len(BOOKS) <1:
      create_books_no_api()
   if books_to_return and len(BOOKS) >= books_to_return >0:
       return BOOKS[:books_to_return]
   return BOOKS

@app.post("/books/login")
async def book_login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
     return {"username":username, "password":password}

@app.get("/header")
async def get_header(random_header: Optional[str] = Header(None)):
      return {"Random_header": random_header}

@app.post("/", status_code=status.HTTP_201_CREATED )
async def create_book(book:Book):
   BOOKS.append(book)
   return book

def create_books_no_api():
    book1= Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa2",title="book1",author="author1",description="description1",rating=1)
    book2= Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="book2", author="author2", description="description2", rating=2)
    book3= Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="book3", author="author3", description="description3", rating=3)
    book4= Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="book4", author="author4", description="description4", rating=4)
    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
      for book in BOOKS:
         if book.id == book_id:
             return book
      raise raise_cannot_be_found_exception()

@app.put("/book/{book_id}")
async def update_book(book_id: UUID, book:Book):
       for index,each_book in  enumerate(BOOKS):
           if each_book.id == book_id:
                BOOKS[index]=book
                return each_book
       raise  raise_cannot_be_found_exception()

@app.delete("/book/{book_id}")
async def delete_book(book_id: UUID):
         for index,each_book in  enumerate(BOOKS):
            if each_book.id == book_id:
                  del BOOKS[index]
                  return {"message":"book deleted"}
         raise   raise_cannot_be_found_exception()


def raise_cannot_be_found_exception():
   return HTTPException(status_code=404, detail="Book not found", headers={"X-Error":"There goes my error"})
