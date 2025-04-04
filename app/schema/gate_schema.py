from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Request Model (what the client sends to your API)
class DeviceRegistrationRequest(BaseModel):
    device_id: str  # Note: The id field is not sent in the request, it's auto-generated
    always_open: bool = False
    last_seen: Optional[datetime] = None
    message: Optional[str] = None
    device: Optional[bool] = False


# Response Model (what you send back as the response)
class DeviceRegistrationResponse(BaseModel):
    id: str
    device_id: str
    always_open: bool = False
    last_seen: Optional[datetime] = None
    message: Optional[str] = None
    device: Optional[bool] = False

    class Config:
        from_attributes = True  # ✅ correct for Pydantic v2
