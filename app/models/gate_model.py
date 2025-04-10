import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship


class DeviceInformation(Base):
    __tablename__ = "gate_device_table"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # ✅ auto UUID
    device_id = Column(String, unique=True, nullable=False)
    always_open = Column(Boolean, default=False)
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
