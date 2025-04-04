from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv


# Force load environment variables
dotenv_loaded = load_dotenv()
print(f".env Loaded: {dotenv_loaded}")  # Should print True if loaded


key = os.getenv("API_KEY")
print(f"Loaded API_KEY: {key}")  # Check if API_KEY is actually loaded


# Load environment variables
load_dotenv()
key = os.getenv("API_KEY", "").strip()
print(key)

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


# def verify_api_key(api_key: str = Security(api_key_header)):
#     """
#     Checks if the provided API key is valid
#     :param api_key:
#     :return:
#     """
#
#     if api_key.strip().lower() != key.lower():
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid API Key"
#         )
#     return api_key

def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is missing"
        )

    # Trim spaces and check the key
    # api_key_cleaned = api_key.strip()
    # key_cleaned = key.strip()
    #
    # print(f"Received API Key: {repr(api_key_cleaned)}")  # Use repr() to reveal hidden characters
    # print(f"Expected API Key: {repr(key_cleaned)}")
    #
    # if api_key != key_cleaned:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Invalid API Key"
    #     )

    return api_key
