from fastapi import APIRouter, HTTPException, Depends
import requests
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.otp_service import generate_otp, validate_otp
from app.services.user_services import USERS
from app.Security.security import verify_api_key
from app.services.user_services import get_user_by_phone_id

router = APIRouter(prefix="/gate", tags=["Gate"])


# Define a request model for OTP validation
class OTPRequest(BaseModel):
    otp: str


RASPBERRY_PI_URL = "http://raspberrypi.local/open-gate"


@router.post("/generate-otp")
def generate_otp_route(
        phone_id: str,
        db: Session = Depends(get_db),
        api_key: str = Depends(verify_api_key)
):
    print(api_key)

    # Check if phone_id exists in the system
    user = db.query(USERS).filter(USERS.phone_id == phone_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Device not registered")

    #  Generate OTP
    otp = generate_otp(phone_id, db)
    return {"phone_id": phone_id, "otp": otp}


@router.post("/validate-otp")
def validate_otp_route(request: OTPRequest, db: Session = Depends(get_db)):
    """Validate OTP received from the request body"""
    if not validate_otp(request.otp, db):  # Extract OTP from request body
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "OTP is valid. Gate can be opened."}


@router.get("/open-gate/{phone_id}")
async def open_gate(phone_id: str, db: Session = Depends(get_db)):
    print(f"Received request to open gate for phone_id: {phone_id}")

    # Use existing function to fetch user

    user = get_user_by_phone_id(phone_id, db)

    if not user:
        print("Unauthorized device attempt")
        raise HTTPException(status_code=403, detail="Unauthorized device")

    # Send request to raspberry pi to open the get if device is authorized
    try:
        response = requests.get(RASPBERRY_PI_URL, timeout=5)
        response.raise_for_status()  # Ensure HTTP request is successful
        print("Gate successfully opened")
        return {"status": "Gate opened"}

    except requests.exceptions.RequestException as e:
        print(f"Failed to open gate: {e}")
        raise HTTPException(status_code=500, detail="Gate control failed")


