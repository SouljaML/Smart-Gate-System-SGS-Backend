from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
print(os.getenv(API_KEY))

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Checks if the provided API key is valid
    :param api_key:
    :return:
    """
    print(f"Received API Key: {api_key}")
    print(f"Expected API Key: {API_KEY}")

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key
