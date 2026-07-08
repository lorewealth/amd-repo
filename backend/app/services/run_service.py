from decimal import Decimal

from fastapi import HTTPException

from backend.app.parser.coverage_parser import parse_header
from backend.app.repositories import run_repository
from backend.app.schemas import BinOut, CoverpointOut, RunDetail, RunListParams
from db import Bin, Coverpoint, Run


def create_run_from_log(session, filename, text, uploaded_by=None):
    if run_repository.get_run_by_filename(session, filename) is not None:
        raise HTTPException(409, f"Fisierul {filename} este deja incarcat in db")
    try:
        report = parse_header(text)
    except ValueError as exc:
        raise HTTPException(400, f"Log invalid {exc}")

    run = Run(
        filename=filename,
        run_date=report.run_datetime,
        result=report.result,
        checks=report.checks,
        overall_coverage=report.overall_coverage,
        uploaded_by=uploaded_by,
    )
    for cp in report.coverpoints:
        coverpoint = Coverpoint(
            name=cp.name,
            coverage=Decimal(cp.coverage),
        )
        for b in cp.bins:
            coverpoint.bins.append(
                Bin(name=b.name, value=b.value, hits=b.hits, hit=b.hit)
            )
        run.coverpoints.append(coverpoint)
    run = run_repository.create_run(session, run)
    coverpoints = [to_coverpointOut(cp) for cp in run.coverpoints]
    total_bins = sum(cp.total_bins for cp in coverpoints)
    total_missed_bins = sum(cp.missed_bins for cp in coverpoints)

    return RunDetail(
        id=run.id,
        filename=run.filename,
        run_date=run.run_date,
        result=run.result,
        overall_coverage=run.overall_coverage,
        checks=run.checks,
        uploaded_at=run.uploaded_at,
        uploaded_by=run.uploaded_by,
        total_bins=total_bins,
        missed_bins=total_missed_bins,
        coverpoints=coverpoints,
    )


def list_runs(session, params: RunListParams):
    return run_repository.get_all_runs(
        session,
        limit=params.limit,
        offset=params.offset,
        result=params.result,
        min_coverage=params.min_coverage,
    )


def to_coverpointOut(cp):
    bins = [BinOut.model_validate(b) for b in cp.bins]
    missed = sum(1 for b in bins if not b.hit)
    return CoverpointOut(
        name=cp.name,
        coverage=cp.coverage,
        total_bins=len(bins),
        missed_bins=missed,
        bins=bins,
    )


def get_run(session, run_id: int):
    run = run_repository.get_run_by_id(session, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    coverpoints = [
        to_coverpointOut(cp) for cp in sorted(run.coverpoints, key=lambda cp: cp.id)
    ]
    total_bins = sum(cp.total_bins for cp in coverpoints)
    missed_bins = sum(cp.missed_bins for cp in coverpoints)

    return RunDetail(
        id=run.id,
        filename=run.filename,
        run_date=run.run_date,
        result=run.result,
        overall_coverage=run.overall_coverage,
        checks=run.checks,
        uploaded_at=run.uploaded_at,
        uploaded_by=run.uploaded_by,
        total_bins=total_bins,
        missed_bins=missed_bins,
        coverpoints=coverpoints,
    )
