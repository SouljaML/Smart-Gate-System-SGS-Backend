from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.services.user_services import create_user, get_all_users, get_user_by_phone_id, get_users_by_device_id
from app.services.gate_device_services import is_device_registered
from app.schema.users_schema import UserCreate, UserResponse

from app.db.database import get_db

router = APIRouter()


# @router.post("/", response_model=UserResponse)
# def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
#     existing_user = get_user_by_phone_id(user.phone_id, db)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Phone ID already exists")
#     return create_user(user, db)
@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    # Ensure the device_id is registered before allowing user creation
    if not is_device_registered(user.device_id, db):
        raise HTTPException(status_code=400, detail="Device not recognized. Please verify first.")

    # Register the new user
    new_user = create_user(user, db)

    return new_user


@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/{phone_id}", response_model=UserResponse)
def get_user(phone_id: str, db: Session = Depends(get_db)):
    user = get_user_by_phone_id(phone_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
