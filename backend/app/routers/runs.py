from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from backend.app.auth.dependencies import check_email, get_current_user
from backend.app.config import get_settings
from backend.app.schemas import RunDetail, RunListParams, RunSummary
from backend.app.services.exceptions import DuplicateRunError, InvalidLogError, RunNotFound
from backend.app.services import run_service
from db import get_db

settings = get_settings()


router = APIRouter()


@router.get(
    "/",
    response_model=list[RunSummary],
    summary="Afisarea totala a rularilor(depinzand de param. limit)",
    responses={
        401: {"description": "Nu sunteti logati in sistem"},
    },
)
def list_runs(params: RunListParams = Depends(), db=Depends(get_db), user: str = Depends(get_current_user)):
    """Returneaza o lista paginata de rulari"""
    return run_service.list_runs(db, params)


@router.get(
    "/{run_id}",
    response_model=RunDetail,
    summary="Afiseaza detalii a unei rulari dupa id",
    responses={
        404: {"description": "Nu a fost gasita aceasta rulare dupa id specificat"},
        401: {"description": "Nu sunteti logati in sistem"},
    },
)
def get_run(run_id: int, db=Depends(get_db), user: str = Depends(get_current_user)):
    """Returneaza detalii unei singure rulari dupa id, inclusiv coverpoints si bins"""
    try:
        return run_service.get_run(db, run_id)
    except RunNotFound as exc:
        raise HTTPException(404, str(exc))

@router.post(
    "/upload",
    status_code=201,
    response_model=RunDetail,
    summary="Incarca un log de simulare in db",
    responses={
        400: {"description": "Fisier invalid(extensie gresita sau continut gol)"},
        413: {
            "description": f"Fisierul depaseste limita permisa: {settings.max_upload_size_view}"
        },
        409: {"description": "Fisier este deja existent in db"},
        401: {"description": "Nu sunteti logati in sistem"}
    },
)
async def upload_run(file: UploadFile = File(...), db: Session = Depends(get_db), user: str = Depends(check_email)):
    """Primeste un fisier .txt cu log de simulare, il parseaza si salveaza rezultatul in baza de date"""
    if file.filename is None or not file.filename.lower().endswith(".txt"):
        raise HTTPException(400, "Sunt acceptate doar fisiere de tip .txt")
    raw = await file.read()
    if not raw:
        raise HTTPException(400, "Fisierul este gol")
    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(413, f"Fisier este prea mare: {settings.max_upload_size_view}")
    text = raw.decode("utf-8")
    try:
        return run_service.create_run_from_log(db, file.filename, text, uploaded_by=user)
    except DuplicateRunError as exc:
        raise HTTPException(409, str(exc))
    except InvalidLogError as exc:
        raise HTTPException(400, str(exc))
