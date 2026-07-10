from fastapi import Depends, HTTPException
from .jwt import oauth2_scheme
from jose import jwt, JWTError

from backend.app.config import get_settings

settings = get_settings()

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(401, "Token invalid sau expirat")
    return payload["sub"]

def check_email(user: str = Depends(get_current_user)) -> str:
    allowed = {e.strip().lower() for e in settings.allowed_email_list.split(",")}
    if user.lower() in allowed:
        return user
    else:
        raise HTTPException(403, "Nu aveti permisiunea de a incarca")
