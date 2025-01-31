import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp_model import OTP
from app.models.users_model import USERS


def generate_otp(phone_id: str, db: Session) -> str:
    otp = str(random.randint(1000, 9999))  # Ensure random module is correctly used
    expiry = datetime.now() + timedelta(minutes=5)

    # Store OTP in the database
    otp_entry = OTP(phone_id=phone_id, otp=otp, expiry=expiry)
    db.merge(otp_entry)  # Merge for update or insert
    db.commit()
    return otp


def validate_otp(otp: str, db: Session) -> bool:
    otp_entry = db.query(OTP).filter(OTP.otp == otp).first()  # Find OTP directly

    if otp_entry and otp_entry.expiry >= datetime.now():
        db.delete(otp_entry)  # Delete OTP after successful validation
        db.commit()
        return True

    return False
