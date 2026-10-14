
from pathlib import Path

import pandas as pd
import pytest

from src.analysis import (
    compare_periods,
    get_safety_summary,
    get_top_airlines,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "airline-safety.csv"


@pytest.fixture
def airline_data():
    return pd.read_csv(DATA_PATH)


def test_dataset_loads_correctly(airline_data):
    assert not airline_data.empty
    assert airline_data.shape == (56, 8)
    assert airline_data["airline"].notna().all()


def test_required_columns_exist(airline_data):
    required = {
        "airline",
        "incidents_85_99",
        "fatal_accidents_85_99",
        "fatalities_85_99",
        "incidents_00_14",
        "fatal_accidents_00_14",
        "fatalities_00_14",
        "avail_seat_km_per_week",
    }
    assert required.issubset(set(airline_data.columns))


def test_safety_summary(airline_data):
    summary = get_safety_summary(airline_data)

    assert summary["airline_count"] == 56
    assert summary["incidents_1985_1999"] == int(
        airline_data["incidents_85_99"].sum()
    )
    assert summary["incidents_2000_2014"] == int(
        airline_data["incidents_00_14"].sum()
    )
    assert summary["fatalities_1985_1999"] == int(
        airline_data["fatalities_85_99"].sum()
    )


def test_period_comparison(airline_data):
    result = compare_periods(airline_data)

    assert len(result) == len(airline_data)
    assert "airline" in result.columns
    assert "Incidents (1985–1999)" in result.columns
    assert "Incidents (2000–2014)" in result.columns
    assert result["Incidents (1985–1999)"].sum() == (
        airline_data["incidents_85_99"].sum()
    )


def test_top_airlines_returns_sorted_results(airline_data):
    result = get_top_airlines(
        airline_data,
        metric="incidents_00_14",
        n=5,
    )

    assert len(result) == 5
    assert result["incidents_00_14"].is_monotonic_decreasing
    assert "airline" in result.columns


def test_invalid_metric_is_rejected(airline_data):
    with pytest.raises(ValueError):
        get_top_airlines(airline_data, metric="unknown_metric")


def test_invalid_top_n_is_rejected(airline_data):
    with pytest.raises(ValueError):
        get_top_airlines(airline_data, n=0)
