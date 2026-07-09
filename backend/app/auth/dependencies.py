from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta

from starlette.exceptions import HTTPException
from backend.app.config import get_settings

settings = get_settings()

def create_access_token(sub: str) -> str:
    payload = {"sub":sub, "exp":datetime.utcnow() + timedelta(hours=24)}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

bearer = HTTPBearer()

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(bearer)) -> str:
    try:
        payload = jwt.decode(cred.credentials, settings.jwt_secret, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(401, "Token invalid sau expirat")
    return payload["sub"]

def check_email(user: str = Depends(get_current_user)) -> str:
    allowed = {e.strip().lower() for e in settings.allowed_email_list.split(",")}
    if user.lower() in allowed:
        return user
    else:
        raise HTTPException(403, "Nu aveti permisiunea de a incarca")
