from sqlalchemy.orm import Session
from sqlalchemy.testing.plugin.plugin_base import logging

from app.schema.gate_schema import DeviceRegistrationRequest
from app.models.users_model import USERS
from app.models.gate_model import DeviceInformation


def createDevice(device: DeviceRegistrationRequest, db: Session):
    try:
        db_device = DeviceInformation(**device.dict())  # Convert Pydantic model to ORM model
        db.add(db_device)
        db.commit()
        db.refresh(db_device)  # Ensure data is refreshed from DB

        # Debugging logs
        print(f"Created Device: {db_device}")

        if not db_device.id or not db_device.device_id:
            raise ValueError("Invalid device data returned from DB")

        return db_device  # Return the DB model, which is correctly mapped to the response
    except Exception as e:
        db.rollback()
        return {"error": "Invalid device data"}


def get_device_by_id(device_id: str, db: Session):
    deviceName = db.query(DeviceInformation).filter(DeviceInformation.device_id == device_id).first()
    return deviceName


def get_all_devices(db: Session):
    return db.query(DeviceInformation).all()


def get_device_by_user_id(user_id: str, db: Session):
    device_by_user_id = db.query(DeviceInformation.join).filter(USERS.id == user_id).first()
    return device_by_user_id


def is_device_registered(device_id: str, db: Session):
    # Query the DeviceInformation model (not the Pydantic schema)
    return db.query(DeviceInformation).filter(DeviceInformation.device_id == device_id).first()
