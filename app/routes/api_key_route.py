from fastapi import Depends, APIRouter

from app.Security.security import verify_api_key

router = APIRouter(prefix="/api", tags=["API_KEY"])


@router.get("/secure-data")
async def get_secure_data(auth: bool = Depends(verify_api_key)):
    msg = {"message": "You are authorized to access this data."}

    return {"auth": auth, **msg}
