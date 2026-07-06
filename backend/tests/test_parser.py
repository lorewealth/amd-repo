import pytest

from app.parser.coverage_parser import parse_file


@pytest.fixture
def test_file1(logs_dir):
    return str(logs_dir / "83_50_overall_FCOV.txt")


@pytest.fixture
def test_file2(logs_dir):
    return str(logs_dir / "78_5_overall_FCOV.txt")


@pytest.fixture
def test_file3(logs_dir):
    return str(logs_dir / "96_25_overall_FCOV.txt")


def test_overall_83_5(test_file1):
    report = parse_file(test_file1)
    assert report.overall_coverage == 83.5


def test_overall_78_5(test_file2):
    report = parse_file(test_file2)
    assert report.overall_coverage == 78.5


def test_total_bins_is_29(test_file1):
    report = parse_file(test_file1)
    total = sum(len(cp.bins) for cp in report.coverpoints)
    assert total == 29


def test_total_miss_is_8_in_83_5(test_file1):
    report = parse_file(test_file1)
    total = sum(1 for cp in report.coverpoints for b in cp.bins if not b.hit)
    assert total == 8


def test_hit_consistency_83_5(test_file1):
    report = parse_file(test_file1)
    for cp in report.coverpoints:
        for b in cp.bins:
            assert (b.hits > 0) == b.hit


def test_hit_consistency_78_5(test_file2):
    report = parse_file(test_file2)
    for cp in report.coverpoints:
        for b in cp.bins:
            assert (b.hits > 0) == b.hit


def test_specific_bin_vec5(test_file3):
    report = parse_file(test_file3)
    cp_vec = next(cp for cp in report.coverpoints if cp.name == "cp_vec")
    bin_5 = next(b for b in cp_vec.bins if b.name == "vec[ 5]")
    assert bin_5.hits == 0
    assert not bin_5.hit
