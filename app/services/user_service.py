import bcrypt
from blueprints import UserSignIn
from fastapi import Depends, HTTPException, status
from logging_module import logger

from typing import Optional, Tuple
from datetime import datetime, timedelta
from jose import jwt
from config.constants import ALGORITHM, SECRET_KEY, DEFAULT_TOKEN_EXPIRY_HOURS, user
from utils.dependencies import get_current_user_id


def create_user_access_token(jwt_payload):
    return create_jwt_with_expiry(jwt_payload)


def create_jwt_with_expiry(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=DEFAULT_TOKEN_EXPIRY_HOURS)
    to_encode.update({"exp": expire})
    to_encode.update({"_id": str(data["_id"])})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def generate_data_token_service(
    data: dict,
):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=DEFAULT_TOKEN_EXPIRY_HOURS)
        to_encode.update({"exp": expire})
        data = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"status_code": 200, "content": {"data": data}}
    except Exception as e:
        logger.debug(f"{e}")
        return {"status_code": 500, "content": {"message": e}}


async def decode_data_token(token):
    try:
        heisman_token_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
        )
        return {"status_code": 200, "content": {"data": heisman_token_data}}
    except Exception as e:
        logger.debug(f"{e}")
        return {"status_code": 500, "content": {"message": e}}


def generate_password_hash(password: str) -> str:
    """Bcrypts a password, returns a hash string"""
    pwd_bytes = password.encode("ascii")
    salt_bytes = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt_bytes).decode("ascii")


async def check_password_hash(attempt, password_hash) -> bool:
    attempt_bytes = attempt.encode("ascii")
    hash_bytes = password_hash.encode("ascii")
    return bcrypt.checkpw(attempt_bytes, hash_bytes)


async def login_for_access_token_service(form_data):
    user, auth_status = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_user_access_token(user)
    return {
        "access_token": access_token,
        "user_id": str(user["_id"]),
        "token_type": "bearer",
    }


async def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[str]]:

    if username != user["email"]:
        return None, "Username does not exist."
    if password != user["password"]:
        return None, "Password is incorrect."

    user["id"] = str(user["_id"])
    return dict(user), "Authentication successful."


async def get_user_via_token_service(user_id: str = Depends(get_current_user_id)):
    try:
        if user:
            return {"status_code": 200, "content": {"data": user}}
        else:
            return {"status_code": 404, "content": {"message": "User not found"}}
    except Exception as e:
        return {"status_code": 500, "content": {"message": str(e)}}


async def signin_service(user_data: UserSignIn):
    try:
        if not user:
            return {"status_code": 404, "content": {"message": "User not found"}}
        if user_data.password == user["password"]:
            name = user.get("full_name", "")
            access_token = create_user_access_token(user)
            return {
                "token": access_token,
                "name": name,
                "email": user["email"],
                "user_id": str(user["_id"]),
            }
        else:
            return {"status_code": 401, "content": {"message": "Invalid password"}}
    except Exception as e:
        return {"status_code": 500, "content": {"message": str(e)}}
