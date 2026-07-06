from sqlalchemy.orm import Session

from models import Run


def get_all_runs(session: Session, limit=20, offset=0):
    return (
        session.query(Run)
        .order_by(Run.run_date.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def get_run_by_id(session: Session, run_id: int):
    return session.get(Run, run_id)
