from sqlalchemy.orm import Session, selectinload

from db import Coverpoint, Run


def get_all_runs(session: Session, limit=20, offset=0, result=None, min_coverage=None):
    q = session.query(Run).order_by(Run.run_date.desc())
    if result:
        q = q.filter(Run.result == result)
    if min_coverage is not None:
        q = q.filter(Run.overall_coverage >= min_coverage)
    return q.limit(limit).offset(offset).all()


def get_run_by_id(session: Session, run_id: int):
    return (
        session.query(Run)
        .options(selectinload(Run.coverpoints).selectinload(Coverpoint.bins))
        .filter(Run.id == run_id)
        .first()
    )
