from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Boolean


class DeviceRegistrationRequest(BaseModel):
    id: str
    device_id: str
    always_open: bool
    last_seen: Optional[datetime] = None

class DeviceRegistrationResponse(BaseModel):
    id: str
    device_id: str
    always_open: bool
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True
