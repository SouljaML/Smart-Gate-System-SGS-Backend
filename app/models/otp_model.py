import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.users_model import USERS  # Import the USERS model
from app.db.database import Base  # Use the correct Base instance


class OTP(Base):
    __tablename__ = "otps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # Ensure a unique PK
    phone_id = Column(String, ForeignKey("users.phone_id"), nullable=False)  # Unique per device
    otp = Column(String, nullable=False)
    expiry = Column(DateTime, default=datetime.utcnow)

    # Relationship with USERS
    user = relationship("USERS", backref="otps")  # Correct class name reference
