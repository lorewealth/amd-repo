from fastapi import APIRouter, Depends

from app.schemas.run import RunDetail, RunListParams, RunSummary
from app.services import run_service
from database import get_db

router = APIRouter()


@router.get("/", response_model=list[RunSummary])
def list_runs(params: RunListParams = Depends(), db=Depends(get_db)):
    return run_service.list_runs(db, params)


@router.get("/{run_id}", response_model=RunDetail)
def get_run(run_id: int, db=Depends(get_db)):
    return run_service.get_run(db, run_id)
