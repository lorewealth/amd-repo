import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto

RE_RESULT = re.compile(r"====\s*(PASSED|FAILED)\s*====\s*checks=(\d+)")
RE_DATE = re.compile(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}\:\d{2} UTC)\]")
RE_SUMMARY = re.compile(r"^\s*(\w+)\s*:\s*([\d.]+)%\s*$")
RE_BIN_VEC = re.compile(
    r"^\s*(vec\[\s*\d+\])\s+([01]{4})\s*:\s*hits=(\d+)\s+(\*\*\* MISS \*\*\*|HIT)"
)
RE_BIN_POP = re.compile(
    r"^\s*(\w+\s*\(\d+\))\s*:\s*hits=(\d+)\s+(\*\*\* MISS \*\*\*|HIT)"
)
RE_BIN_EN_VOTE = re.compile(
    r"^\s*(\w+=\d+)\s*:\s*hits=(\d+)\s+(\*\*\* MISS \*\*\*|HIT)"
)
RE_BIN_X_EN_VOTE = re.compile(
    r"^\s*(\([^)]+\))\s*:\s*hits=(\d+)\s+(\*\*\* MISS \*\*\*|HIT)"
)
RE_BINS_HEADER = re.compile(r"^\s*(\w+)\s+.*bins")


@dataclass
class Coverpoint:
    name: str
    coverage: float
    bins: list = field(default_factory=list)


@dataclass
class Bin:
    name: str
    hits: int
    hit: bool
    value: str | None = None


@dataclass
class Returnabil:
    run_date: str | None = None
    run_datetime: datetime | None = None
    result: str | None = None
    checks: int | None = None
    overall_coverage: float | None = None
    coverpoints: list[Coverpoint] = field(default_factory=list)


class State(Enum):
    BEFORE_COVERAGE = auto()
    IN_SUMMARY = auto()
    IN_BINS = auto()
    DONE = auto()


def parse_file(fisier):
    with open(fisier) as f:
        text = f.read()
    return parse_header(text)


def parse_header(text):
    run_date: str | None = None
    run_datetime: datetime | None = None
    result: str | None = None
    checks: int | None = None
    overall_coverage: float | None = None
    coverpoints = []
    current_cp: Coverpoint | None = None
    cp_name = None

    state = State.BEFORE_COVERAGE

    for line in text.splitlines():
        match state:
            case State.BEFORE_COVERAGE:
                n = RE_DATE.match(line)
                if n:
                    run_date = n.group(1)
                    assert run_date is not None
                    run_datetime = datetime.strptime(run_date, "%Y-%m-%d %H:%M:%S UTC")
                m = RE_RESULT.search(line)
                if m:
                    result, checks = m.group(1), int(m.group(2))
                if "Functional Coverage" in line:
                    state = State.IN_SUMMARY
            case State.IN_SUMMARY:
                if "bins" in line:
                    state = State.IN_BINS
                    m = RE_BINS_HEADER.match(line)
                    if m:
                        cp_name = m.group(1)
                    current_cp = next(cp for cp in coverpoints if cp.name == cp_name)
                else:
                    m = RE_SUMMARY.match(line)
                    if m:
                        name, pct = m.group(1), float(m.group(2))
                        if name == "OVERALL":
                            overall_coverage = pct
                        else:
                            coverpoints.append(Coverpoint(name=name, coverage=pct))
            case State.IN_BINS:
                if "===========================================" in line:
                    state = State.DONE
                    break
                elif "bins" in line:
                    m = RE_BINS_HEADER.match(line)
                    if m:
                        cp_name = m.group(1)
                    current_cp = next(cp for cp in coverpoints if cp.name == cp_name)
                else:
                    m1 = RE_BIN_VEC.match(line)
                    m2 = RE_BIN_POP.match(line)
                    m3 = RE_BIN_EN_VOTE.match(line)
                    m4 = RE_BIN_X_EN_VOTE.match(line)

                    if m1 and current_cp is not None:
                        name, value, hits, status = m1.groups()
                        hit = status == "HIT"
                        current_cp.bins.append(
                            Bin(name=name, hits=int(hits), hit=hit, value=value)
                        )
                    elif m2 and current_cp is not None:
                        name, hits, status = m2.groups()
                        hit = status == "HIT"
                        current_cp.bins.append(Bin(name=name, hits=int(hits), hit=hit))
                    elif m3 and current_cp is not None:
                        name, hits, status = m3.groups()
                        hit = status == "HIT"
                        current_cp.bins.append(Bin(name=name, hits=int(hits), hit=hit))
                    elif m4 and current_cp is not None:
                        name, hits, status = m4.groups()
                        hit = status == "HIT"
                        current_cp.bins.append(Bin(name=name, hits=int(hits), hit=hit))
    return Returnabil(
        run_date=run_date,
        run_datetime=run_datetime,
        result=result,
        checks=checks,
        overall_coverage=overall_coverage,
        coverpoints=coverpoints,
    )


if __name__ == "__main__":
    import json
    import sys
    from dataclasses import asdict

    path = sys.argv[1]
    result = parse_file(path)
    print(json.dumps(asdict(result), indent=2, default=str))
