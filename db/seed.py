from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.parser.coverage_parser import parse_file
from db import Bin, Coverpoint, Run, engine


def main():
    fisiere_log = sorted(Path("logs/").glob("*.txt"))

    with Session(engine) as session:
        print("[ ---- Seed.py ---- ]")
        for path_fisier in fisiere_log:
            den_fisier = path_fisier.name.lower()
            res = session.query(Run).filter_by(filename=den_fisier).first()
            if res:
                print(f" [-] Fisier \"{den_fisier}\" a fost deja parsat in db")
                continue
            try:
                report = parse_file(path_fisier)
            except ValueError as e:
                print(f" [!] Fisier \"{den_fisier}\" -> error {e}")
                continue
            run = Run(
                filename=den_fisier,
                run_date=report.run_datetime,
                result=report.result,
                checks=report.checks,
                overall_coverage=report.overall_coverage,
                uploaded_by="seed.py",
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
            print(f" [+] Fisier \"{den_fisier}\" a fost incarcat cu succes")
    print("[ ----------------- ]")

if __name__ == "__main__":
    main()
