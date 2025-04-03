from sqlalchemy.orm import Session
from app.models.users_model import USERS
from app.schema.users_schema import UserCreate
from app.schema.gate_schema import DeviceRegistrationRequest


def create_user(user: UserCreate, db: Session):
    db_user = USERS(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(USERS).all()


def get_user_by_phone_id(phone_id: str, db: Session):
    return db.query(USERS).filter(USERS.phone_id == phone_id).first()



