from fastapi import APIRouter, HTTPException, Depends, WebSocket
import requests
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.otp_service import generate_otp, validate_otp
from app.services.user_services import USERS
from app.Security.security import verify_api_key
from app.services.user_services import get_user_by_phone_id
from app.services.gate_device_services import get_device_by_user_id, get_device_by_id, createDevice, get_all_devices
from typing import List
from app.schema.gate_schema import DeviceRegistrationRequest, DeviceRegistrationResponse
from app.schema.users_schema import UserCreate


router = APIRouter(prefix="/gate", tags=["Gate"])

# List to store connected devices Websocket clients (Raspberry Pi Devices)
connected_clients: List[WebSocket] = []


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


@router.websocket("ws/gate")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection for raspberry pi to receive commands to open the gate"""
    await WebSocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except:
        connected_clients.remove(websocket)


@router.post("/open")
async def open_gate(user: UserCreate, db: Session = Depends(get_db)):
    """Send a gate open request to all connected Raspberry Pi clients after validation"""
    # Check if the user has a registered device
    device = get_device_by_user_id(user.device_id, db)
    if not device:
        raise HTTPException(status_code=403, detail="No registered device linked to this phone")

    # Send the open command only if the user has a linked device
    for client in connected_clients:
        try:
            await client.send_text("open_gate")  # Send command to open gate
        except:
            connected_clients.remove(client)  # Remove disconnected clients

    return {"success": True, "message": "Gate open command sent"}


@router.post("/device_registration", response_model=DeviceRegistrationResponse)
async def register_device(device: DeviceRegistrationRequest, db: Session = Depends(get_db),
                          _: str = Depends(verify_api_key)):
    # Check if the device is already registered
    existing_device = get_device_by_id(device.device_id, db)

    if existing_device:
        # Return a response with a message and a device flag
        return DeviceRegistrationResponse(
            id=existing_device.id,
            device_id=existing_device.device_id,
            message="Device already registered",
            device=True  # Indicate that this device exists
        )

    # Else, register the new device
    new_device = createDevice(device, db)

    if isinstance(new_device, dict) and "error" in new_device:
        # Handle error case
        raise HTTPException(status_code=400, detail=new_device["error"])

    return new_device


@router.get("/{device_id}", response_model=DeviceRegistrationResponse)
def get_device(device_id: str, db: Session = Depends(get_db),
               _: str = Depends(verify_api_key)):
    device = get_device_by_id(device_id, db)

    if not device:
        raise HTTPException(status_code=400, detail="Device ID does not exist")

    return device


@router.get("/device/{user_id}", response_model=DeviceRegistrationResponse)
def device_by_user_id(user_id: str, db: Session = Depends(get_db),
                      _: str = Depends(verify_api_key)):
    device = get_device_by_user_id(user_id, db)

    if not device:
        raise HTTPException(status_code=400, detail="device not found")

    return device


@router.get("/", response_model=List[DeviceRegistrationResponse])
def all_devices(db: Session = Depends(get_db),
                _: str = Depends(verify_api_key)):
    devices = get_all_devices(db)

    if not devices:
        print("No devices found in the database.")
        raise HTTPException(status_code=404, detail="No devices found")

    return devices
