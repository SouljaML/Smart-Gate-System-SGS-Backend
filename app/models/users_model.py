import uuid
from sqlalchemy import Column, String, ForeignKey
from app.db.database import Base
from app.models.gate_model import DeviceInformation
from sqlalchemy.orm import relationship


class USERS(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # Auto-generate UUID
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_id = Column(String, unique=True, nullable=False)
    car_reg = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    device_id = Column(ForeignKey(DeviceInformation.device_id), nullable=True)

    device = relationship("DeviceInformation", back_populates="users")


