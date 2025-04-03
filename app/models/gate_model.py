import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship


class DeviceInformation(Base):
    __tablename__ = "gate_device_table"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # Auto-generate UUID
    device_id = Column(String, nullable=False)
    always_open = Column(Boolean, default=False)
    last_seen = Column(DateTime, default=datetime.utcnow)

    users = relationship("USERS", back_populates="device")


