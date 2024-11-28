from config.constants import oauth2_scheme, user
from fastapi import Depends, HTTPException, status
from logging_module import logger


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return user["_id"]
    except Exception as e:
        logger.error(f"Error in get current user id: {e}")
        raise credentials_exception
