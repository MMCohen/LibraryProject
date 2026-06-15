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

class UpdateMember(BaseModel):
    name: str = None
    email: str = None


@router.post("/members")
def create_member(data: NewMember):
    update_data = data.model_dump()
    try:
        new_id = member_db.create_member(update_data)
    except EmailExist:
        raise HTTPException(status_code=409, detail="email already exist!")
    return {"new_id": new_id}


@router.get("/members")
def get_all_members():
    return member_db.get_all_members()


@router.get("/members/{id}")
def get_member_by_id(id: int):
    member =  member_db.get_member_by_id(id)
    if not member:
        raise HTTPException(status_code=404, detail=f"member id: {id} not found!")
    return member


@router.put("/members/{id}")
def update_member(id: int, data: UpdateMember):
    update_data = data.model_dump(exclude_unset=True)
    is_update = member_db.update_member(id, update_data)
    if not is_update:
        raise HTTPException(status_code=404, detail="member not found or not updated ")
    return {"message": "updated successfully"}

