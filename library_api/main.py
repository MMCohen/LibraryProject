import uvicorn

from database.db_connection import DbConnection
from fastapi import FastAPI
from library_api.routes import book_routes, member_routes, report_routes

connector = DbConnection()
connector.create_tables()


app = FastAPI()

app.include_router(book_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

