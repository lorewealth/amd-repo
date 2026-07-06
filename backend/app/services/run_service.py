from fastapi import HTTPException

from app.repositories import run_repository


def list_runs(session, limit=20, offset=0):
    return run_repository.get_all_runs(session, limit, offset)


def get_run(session, run_id: int):
    run = run_repository.get_run_by_id(session, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
