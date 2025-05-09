from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_id: str
    car_reg: Optional[str] = None
    email: Optional[str] = None
    device_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_id: str
    car_reg: Optional[str] = None
    email: Optional[str] = None
    device_id: Optional[str] = None

    class Config:
        from_attributes = True



