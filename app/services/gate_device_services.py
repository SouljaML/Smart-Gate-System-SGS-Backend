from sqlalchemy.orm import Session
from app.schema.gate_schema import DeviceRegistrationRequest


def createDevice(device: DeviceRegistrationRequest, db: Session):
    db_device = DeviceRegistrationRequest(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return db_device


def get_device_by_id(device_id: str, db: Session):
    deviceName = db.query(DeviceRegistrationRequest).filter(DeviceRegistrationRequest.device_id == device_id).first()
    return deviceName


def get_all_devices(db: Session):
    return db.query(DeviceRegistrationRequest).all()