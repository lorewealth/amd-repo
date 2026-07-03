from datetime import datetime
from os import path
from sys import argv, exit

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.parser.coverage_parser import parse_file
from database import Bin, Coverpoint, Run, engine

path_fisier = "logs/" + argv[1] + "_overall_FCOV.txt"
den_fisier = path.basename(path_fisier).lower()

with Session(engine) as session:
    cond = select(Run.filename)
    res = session.execute(cond).scalars().all()
    if den_fisier in res:
        print(f'Fisier "{den_fisier}" a fost deja parsat in db')
        exit(0)

report = parse_file(path_fisier)
with Session(engine) as session:
    run = Run(
        filename=den_fisier,
        run_date=datetime.fromisoformat(report["run_datetime"]),
        result=report["result"],
        checks=report["checks"],
        overall_coverage=report["overall_coverage"],
    )
    for cp in report["coverpoints"]:
        c = Coverpoint(name=cp["name"], coverage=cp["coverage"])
        c.bins = [
            Bin(name=b["name"], value=b["value"], hits=b["hits"], hit=b["hit"])
            for b in cp["bins"]
        ]
        run.coverpoints.append(c)
    session.add(run)
    session.commit()
