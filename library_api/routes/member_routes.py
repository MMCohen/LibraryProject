from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from library_api.database.db_connection import DbConnection
from library_api.database.member_db import MemberDb, EmailExist

connection = DbConnection()
member_db = MemberDb(connection)

router = APIRouter()

class NewMember(BaseModel):
    name: str
    email: str


@router.post("/members")
def create_member(data: NewMember):
    update_data = data.model_dump()
    try:
        new_id = member_db.create_member(update_data)
    except EmailExist:
        raise HTTPException(status_code=409, detail="email already exist!")
    return {"new_id": new_id}



