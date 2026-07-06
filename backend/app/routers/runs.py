from fastapi import APIRouter, Depends

from app.services import run_service
from database import get_db

router = APIRouter()


@router.get("/")
def list_runs(limit: int = 20, offset: int = 0, db=Depends(get_db)):
    return run_service.list_runs(db, limit, offset)


@router.get("/{run_id}")
def get_run(run_id: int, db=Depends(get_db)):
    return run_service.get_run(db, run_id)
