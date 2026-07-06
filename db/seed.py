from pathlib import Path
from sys import path

path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from sqlalchemy.orm import Session

from backend.app.parser.coverage_parser import parse_file
from backend.database import engine
from backend.models import Bin, Coverpoint, Run


def main():
    fisiere_log = sorted(Path("logs/").glob("*.txt"))

    with Session(engine) as session:
        for path_fisier in fisiere_log:
            den_fisier = path_fisier.name.lower()
            res = session.query(Run).filter_by(filename=den_fisier).first()
            if res:
                print(f'Fisier "{den_fisier}" a fost deja parsat in db')
                continue
            report = parse_file(path_fisier)
            run = Run(
                filename=den_fisier,
                run_date=report.run_datetime,
                result=report.result,
                checks=report.checks,
                overall_coverage=report.overall_coverage,
            )
            for cp in report.coverpoints:
                c = Coverpoint(name=cp.name, coverage=cp.coverage)
                c.bins = [
                    Bin(name=b.name, value=b.value, hits=b.hits, hit=b.hit)
                    for b in cp.bins
                ]
                run.coverpoints.append(c)
            session.add(run)
            session.commit()


if __name__ == "__main__":
    main()
