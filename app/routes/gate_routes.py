import json

from fastapi import APIRouter, \
    HTTPException, \
    Depends, \
    WebSocket
import requests
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

from app.db.database import get_db
from app.services.otp_service import generate_otp, validate_otp
from app.services.user_services import USERS
from app.Security.security import verify_api_key
from app.services.user_services import get_user_by_phone_id
from app.services.gate_device_services import get_device_by_phone_id, \
    get_device_by_id, \
    createDevice, \
    get_all_devices, \
    get_device_by_user_id
from typing import List, Dict
from app.schema.gate_schema import DeviceRegistrationRequest, \
    DeviceRegistrationResponse, \
    GateModeRequest
from app.schema.users_schema import UserCreate

router = APIRouter(prefix="/gate", tags=["Gate"])

# List to store connected devices Websocket clients (Raspberry Pi Devices)
# connected_clients: List[WebSocket] = []
connected_clients: Dict[str, WebSocket] = {}


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
def validate_otp_route(request: OTPRequest, db: Session = Depends(get_db),
                       _: str = Depends(verify_api_key)):
    """Validate OTP received from the request body"""
    if not validate_otp(request.otp, db):  # Extract OTP from request body
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "OTP is valid. Gate can be opened."}


@router.get("/open-gate/{phone_id}")
async def open_gate(phone_id: str, db: Session = Depends(get_db),
                    _: str = Depends(verify_api_key)):
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


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket connection for Raspberry Pi to receive commands to open the gate"""
    await websocket.accept()
    # connected_clients.append(websocket)
    connected_clients[client_id] = websocket
    print(f"Connected clients: {client_id}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {client_id}: {data}")
            # Optional: respond to client or handle command
            # await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        print(f"Client disconnected:{client_id}")
        if client_id in connected_clients:
            del connected_clients[client_id]
    except Exception as e:
        print(f"Websocket error for client {client_id}: {e}")
        if client_id in connected_clients:
            del connected_clients[client_id]
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)


# "ws://localhost:8000/ws"

async def send_command_to_client(client_id: str, command: Dict):
    """Sends a JSON command to the specific connected client"""
    if client_id in connected_clients:
        websocket = connected_clients[client_id]

        try:
            await websocket.send_text(json.dumps(command))
            print(f"Send command to {command} to {client_id}")
            return True
        except WebSocketDisconnect:
            print(f"Error: Connection closed for client {client_id}")
            del connected_clients[client_id]
            return False
        except Exception as e:
            print(f"Error sending command to {client_id}: {e}")
            return False
    else:
        print(f"Client {client_id} not connected")
        return False


@router.post("/open")
async def open_gate(phone_id: str, db: Session = Depends(get_db),
                    _: str = Depends(verify_api_key)):
    """Send a gate open request to all connected Raspberry Pi clients after validation"""
    # Check if the user has a registered device
    device = device_by_phone_id(phone_id, db)
    print(f'This is the expected device id: {device.device_id}')
    if not device:
        raise HTTPException(status_code=403,
                            detail="No registered device linked to this phone")

    print(f"[DEBUG] Found device: {device.device_id}")

    # Send the open command only if the user has a linked device
    command = {"command": "open-gate"}
    success = await send_command_to_client(device.device_id, command)

    if success:
        return {"success": True, "message": "Gate open command sent"}
    else:
        raise HTTPException(status_code=400,
                            detail=f"Device {device.device_id} not connected or error sending command")


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


@router.get("/device/{phone_id}")
def device_by_phone_id(phone_id: str, db: Session = Depends(get_db),
                      _: str = Depends(verify_api_key)):
    device = get_device_by_phone_id(phone_id, db)

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


@router.post("/mode")
def set_gate_mode(mode: GateModeRequest, db: Session = Depends(get_db),
                  _: str = Depends(verify_api_key)):
    device = get_device_by_id(mode.device_id, db)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device.always_open = mode.always_open
    db.commit()
    return {"message": "Gate mode updated successfully",
            "device_id": device.device_id, "always_open": device.always_open}


@router.get("/mode/{device_id}")
def get_gate_mode(device_id: str, db: Session = Depends(get_db),
                  _: str = Depends(verify_api_key)):
    device = get_device_by_id(device_id, db)

    if not device:
        raise HTTPException(status_code=404, detail="Device Not found")

    return {"message": device.device_id, "always_open": device.always_open}


@router.post("/close/{device_id}")
def close_gate(device_id: str, db: Session = Depends(get_db),
               _: str = Depends(verify_api_key)):
    device = get_device_by_id(device_id, db)

    if not device:
        raise HTTPException(status_code=404, detail="Device Not found")

    if not device.always_open:
        raise HTTPException(status_code=400, detail="Gate is in normal mode, auto close is active")

    # Perform get closing logic on this section, not yet implemented, we will a send to ESP32 to close
    device.always_open = False
    db.commit()

    return {"message": "Gate closing triggered", "device_id": device.device_id}


def auto_close_gate(device_id: str, db: Session):
    device = get_device_by_id(device_id, db)

    if device and not device.always_open:
        #  Perform auto-close operation here
        print(f"auto-closing gate for device {device.device_id}...")
