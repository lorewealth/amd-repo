from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from backend.app.config import get_settings
from backend.app.routers import runs, auth

settings = get_settings()

app = FastAPI(
    title="Functional Coverage Dashboard",
    description="API pentru upload si vizualizare rezultatelor de coverage functional din simulari VCS.",
    version="1.0.0",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.jwt_secret
)

app.include_router(runs.router, prefix="/runs", tags=["runs"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def health_check():
    return {"status": "ok"}
