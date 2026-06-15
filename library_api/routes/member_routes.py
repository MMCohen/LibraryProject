from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from library_api.database.db_connection import DbConnection
from library_api.database.member_db import MemberDb

#import exceptions
from library_api.database.member_db import EmailNotExist, MemberNotExist

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
    except EmailNotExist:
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


@router.put("/members/{id}/deactivate")
def deactivate_member(id: int):
    try:
        is_deactivate = member_db.deactivate_member(id)

    except MemberNotExist:  #todo: maybe add exception MemberAlreadyDeactivate
        raise HTTPException(status_code=404, detail=f"Member id {id} not found!")

    if is_deactivate:
        return {"Message": f"member id {id} deactivate"}

    raise HTTPException(status_code=400, detail="somthing went wrong")


@router.put("/members/{id}/activate")
def activate_member(id: int):
    try:
        is_activate = member_db.activate_member(id)

    except MemberNotExist:  #todo: maybe add exception MemberAlreadyActivate
        raise HTTPException(status_code=404, detail=f"Member id {id} not found!")

    if is_activate:
        return {"Message": f"member id {id} activate successfully"}

    raise HTTPException(status_code=400, detail="somthing went wrong")





