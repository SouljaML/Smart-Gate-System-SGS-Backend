from sqlalchemy import Column, String
from app.db.database import Base


class PIN(Base):
    __tablename__ = "pins"

    id = Column(String, primary_key=True, index=True)
    pin = Column(String, nullable=False)
