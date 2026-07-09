from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from backend.app.config import get_settings
from backend.app.auth.dependencies import create_access_token
from fastapi import APIRouter

oauth = OAuth()
settings = get_settings()
router = APIRouter()

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    client_kwargs={"scope":"openid email profile"}
)

@router.get("/login")
async def login(request:Request):
    redirect_uri = request.url_for("callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="callback")
async def callback(request:Request):
    token=await oauth.google.authorize_access_token(request)
    info = token["userinfo"]
    jwt = create_access_token(sub=info["email"])
    return {"access_token": jwt, "token_type":"bearer"}
