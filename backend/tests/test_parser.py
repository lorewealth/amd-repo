from app.parser.coverage_parser import parse_file


def test_overall_83_5():
    report = parse_file("../backend/logs/83_50_overall_FCOV.txt")
    assert report["overall_coverage"] == 83.5


def test_overall_78_5():
    report = parse_file("../backend/logs/78_5_overall_FCOV.txt")
    assert report["overall_coverage"] == 78.5


def test_total_bins_is_29():
    report = parse_file("../backend/logs/83_50_overall_FCOV.txt")
    total = sum(len(cp["bins"]) for cp in report["coverpoints"])
    assert total == 29


def test_total_miss_is_8_in_83_5():
    report = parse_file("../backend/logs/83_50_overall_FCOV.txt")
    total = sum(1 for cp in report["coverpoints"] for b in cp["bins"] if not b["hit"])
    assert total == 8


def test_hit_consistency_83_5():
    report = parse_file("../backend/logs/83_50_overall_FCOV.txt")
    for cp in report["coverpoints"]:
        for b in cp["bins"]:
            assert (b["hits"] > 0) == b["hit"]


def test_hit_consistency_78_5():
    report = parse_file("../backend/logs/78_5_overall_FCOV.txt")
    for cp in report["coverpoints"]:
        for b in cp["bins"]:
            assert (b["hits"] > 0) == b["hit"]


def test_specific_bin_vec5():
    report = parse_file("../backend/logs/96_25_overall_FCOV.txt")
    cp_vec = next(cp for cp in report["coverpoints"] if cp["name"] == "cp_vec")
    bin_5 = next(b for b in cp_vec["bins"] if b["name"] == "vec[ 5]")
    assert bin_5["hits"] == 0
    assert not bin_5["hit"]
