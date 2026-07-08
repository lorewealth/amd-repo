from fastapi import HTTPException

from backend.app.repositories import run_repository
from backend.app.schemas import BinOut, CoverpointOut, RunDetail, RunListParams


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
