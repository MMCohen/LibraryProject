import uvicorn
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from library_api.database.book_db import BookDb
from library_api.database.db_connection import DbConnection

connection = DbConnection()
bookdb = BookDb(connection)

router = APIRouter()

class NewBook(BaseModel):
    title: str
    author: str
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"]


class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"] | None = None


@router.get("/books")
def get_all_books():
    return bookdb.get_all_books()


@router.post("/books")
def create_book(data: NewBook):
    data = data.model_dump()
    return bookdb.create_book(data)


@router.get("/books/{id}")
def get_book_by_id(id):
    book = bookdb.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail=f"book id: {id} not found!")
    else:
        return book


@router.put("/books/{id}")
def update_book_by_id(id: int, data: UpdateBook):
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400 , detail="no data entered to update")

    is_update = bookdb.update_book(id, update_data)

    if not is_update:
        raise HTTPException(status_code=404, detail="Book not found or not updated")

    return {"message": "updated successfully"}


@router.put("/books/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    pass


@router.put("/books/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    pass



if __name__ == "__main__":
    print("hello from book routs")
