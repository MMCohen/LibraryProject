
from fastapi import APIRouter
from library_api.database.book_db import BookDb

bookdb = BookDb()



router = APIRouter()

@router.get("/books")
def get_all_books():
    return bookdb.get_all_books()


if __name__ == "__main__":
    print("hello from book routs")
