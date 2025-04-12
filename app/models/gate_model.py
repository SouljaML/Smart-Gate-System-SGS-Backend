import uuid
from datetime import datetime

from enum import Enum

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship


class DeviceInformation(Base):
    __tablename__ = "gate_device_table"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # ✅ auto UUID
    device_id = Column(String, unique=True, nullable=False)
    always_open = Column(Boolean, default=False)
    status = Column(String, default="closed")
    last_seen = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=True)
    device = Column(Boolean, nullable=True)

    users = relationship("USERS", back_populates="device")

    def __repr__(self):
        return f"<DeviceInformation(id={self.id}, device_id={self.device_id}, always_open={self.always_open})>"

    def __str__(self):
        return f"DeviceInformation(device_id={self.device_id})"

    def __repr__(self):
        return self.__str__()


# --------------Enum valid for gate commands------------------*
class gateCommand(str, Enum):
    open_gate = "open-gate"
    close_gate = "close-gate"
    always_open = "always-open"



