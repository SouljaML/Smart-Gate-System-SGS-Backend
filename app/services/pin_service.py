from sqlalchemy.orm import Session
from app.models.pin_model import PIN


def create_or_update_pin(pin_id: str, pin: str, db: Session):
    """
    Create or update a PIN entry.
    """
    pin_entry = db.query(PIN).filter(PIN.id == pin_id).first()
    if pin_entry:
        pin_entry.pin = pin  # Update existing PIN
    else:
        pin_entry = PIN(id=pin_id, pin=pin)  # Create new PIN
        db.add(pin_entry)
    db.commit()


def validate_pin(pin_id: str, pin: str, db: Session) -> bool:
    """
    Validate if the provided PIN matches the stored PIN.
    """
    pin_entry = db.query(PIN).filter(PIN.id == pin_id).first()
    return pin_entry is not None and pin_entry.pin == pin


def delete_pin(pin_id: str, db: Session):
    """
    Delete a PIN entry.
    """
    pin_entry = db.query(PIN).filter(PIN.id == pin_id).first()
    if pin_entry:
        db.delete(pin_entry)
        db.commit()
