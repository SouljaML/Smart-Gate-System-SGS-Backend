from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.testing.plugin.plugin_base import logging

from app.schema.gate_schema import DeviceRegistrationRequest
from app.models.users_model import USERS
from app.models.gate_model import DeviceInformation

from fastapi.logger import logger


def createDevice(device: DeviceRegistrationRequest, db: Session):
    try:
        db_device = DeviceInformation(**device.dict())  # Convert Pydantic model to ORM model
        db.add(db_device)
        db.commit()
        db.refresh(db_device)  # Ensure data is refreshed from DB

        # Debugging logs
        logger.info(f"Device created: ID={db_device.id}, DeviceID={db_device.device_id}")

        if not db_device.id or not db_device.device_id:
            logger.warning(f"Device created but missing ID or device id.")
            raise ValueError("Invalid device data returned from DB")

        return db_device  # Return the DB model, which is correctly mapped to the response
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create device: {e}")
        return {"error": "Invalid device data"}


def get_device_by_id(device_id: str, db: Session):
    deviceName = db.query(DeviceInformation).filter(DeviceInformation.device_id == device_id).first()
    return deviceName


def get_all_devices(db: Session):
    return db.query(DeviceInformation).all()


def get_device_by_phone_id(phone_id: str, db: Session):
    device = (
        db.query(DeviceInformation)
            .join(USERS, USERS.device_id == DeviceInformation.device_id)  # Join condition
            .filter(USERS.phone_id == phone_id)  # Filter by phone_id
            .first()
    )
    return device


def is_device_registered(device_id: str, db: Session):
    # Query the DeviceInformation model (not the Pydantic schema)
    return db.query(DeviceInformation).filter(DeviceInformation.device_id == device_id).first()


def get_device_by_user_id(user_id: str, db: Session):
    device = (db.query(USERS)
              .join(DeviceInformation, DeviceInformation.device_id == USERS.device_id)
              .filter(USERS.id == user_id)
              .first()
              )
    return device


def update_gate_status(device_id: str, status: str, db: Session):
    device = get_device_by_id(device_id, db)

    if device:
        device.status = status
        device.last_seen = datetime.utcnow()
        db.commit()
        db.refresh(device)
        return device
    return None
