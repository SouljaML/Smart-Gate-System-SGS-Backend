from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("API_KEY", "").strip()
API_KEY_NAME = "X-API-KEY"
# print(API_KEY)

api_key_header = APIKeyHeader(name="API_KEY_NAME", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key missing"
        )
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    return api_key
