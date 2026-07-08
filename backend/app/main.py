from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import get_settings
from backend.app.routers import runs

settings = get_settings()

app = FastAPI(
    title="Functional Coverage Dashboard",
    description="API pentru upload si vizualizare rezultatelor de coverage functional din simulari VCS.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(runs.router, prefix="/runs", tags=["runs"])


@app.get("/")
def health_check():
    return {"status": "ok"}
