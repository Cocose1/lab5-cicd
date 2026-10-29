from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

_db: dict[int, dict] = {1: {"id": 1, "name": "Alice", "email": "alice@example.com"}}
_next_id = 2


class UserIn(BaseModel):
    name: str
    email: str


@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id not in _db:
        raise HTTPException(status_code=404, detail="User not found")
    return _db[user_id]


@router.post("", status_code=201)
def create_user(user: UserIn):
    global _next_id
    record = {"id": _next_id, **user.model_dump()}
    _db[_next_id] = record
    _next_id += 1
    return record


@router.put("/{user_id}")
def update_user(user_id: int, user: UserIn):
    if user_id not in _db:
        raise HTTPException(status_code=404, detail="User not found")
    _db[user_id] = {"id": user_id, **user.model_dump()}
    return _db[user_id]


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in _db:
        raise HTTPException(status_code=404, detail="User not found")
    del _db[user_id]
