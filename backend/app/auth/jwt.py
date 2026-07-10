from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2AuthorizationCodeBearer
from backend.app.config import get_settings

settings = get_settings()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/auth/login",
    tokenUrl="/auth/token",
    scopes={"openid":"OpenID", "email":"Email", "profile":"Profile"},
)

def create_access_token(sub: str) -> str:
    payload = {"sub":sub, "exp":datetime.now(timezone.utc) + timedelta(hours=24)}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
