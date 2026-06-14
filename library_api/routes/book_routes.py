
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from library_api.database.book_db import BookDb
from library_api.database.db_connection import DbConnection

connection = DbConnection()
bookdb = BookDb(connection)

router = APIRouter()

class NewBook(BaseModel):
    title: str
    author: str
    genre: str


class UpdateBook(BaseModel):
    title: str = None
    author: str = None
    genre: str = None


@router.get("/books")
def get_all_books():
    return bookdb.get_all_books()


@router.post("/books")
def create_book(data: NewBook):
    data = data.model_dump()

    if data["genre"] not in ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'):
        raise HTTPException(status_code=400, detail="genre must be from: Fiction, Non-Fiction, Science, History, Other")

    return bookdb.create_book(data)


@router.get("/books/{id}")
def get_book_by_id(id):
    book = bookdb.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail=f"book id: {id} not found!")
    else:
        return book


@router.put("/books/{id}")
def update_book_by_id(id, data: UpdateBook):
    is_update = bookdb.update_book(id, data.model_dump(exclude_none=True))
    if not is_update:
        raise HTTPException(status_code=400, detail="could not be updated")
    return is_update



if __name__ == "__main__":
    print("hello from book routs")
