from authlib.integrations.starlette_client import OAuth
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from backend.app.config import get_settings
from backend.app.auth.jwt import create_access_token
from fastapi import APIRouter, Form
import secrets

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
    request.session["swagger_redirect_uri"] = request.query_params.get("redirect_uri")
    request.session["swagger_state"] = request.query_params.get("state")
    redirect_uri = request.url_for("callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

_auth_coduri: dict[str, str] = {}

@router.get("/callback", name="callback")
async def callback(request:Request):
    token=await oauth.google.authorize_access_token(request)
    info = token["userinfo"]
    jwt = create_access_token(sub=info["email"])

    code = secrets.token_urlsafe(32)
    _auth_coduri[code] = jwt

    swagger_redirect_uri = request.session.pop("swagger_redirect_uri", None)
    swagger_state = request.session.pop("swagger_state", None)
    if swagger_redirect_uri:
        return RedirectResponse(f"{swagger_redirect_uri}?code={code}&state={swagger_state}")
    return {"access_token": jwt, "token_type":"bearer"}

@router.post(
    "/token",
    responses={
        400: {"description":"Token invalid sau expirat"},
    }
)
async def token(code: str = Form(...)):
    jwt = _auth_coduri.pop(code, None)
    if not jwt:
        raise HTTPException(400, "Token invalid sau expirat")
    return {"access_token": jwt, "token_type":"bearer"}
