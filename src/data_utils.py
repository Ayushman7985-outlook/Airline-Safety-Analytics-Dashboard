"""Dataset generation, loading, and cleaning utilities."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["Question", "Option", "Region", "Age Group", "Timestamp"]


def generate_synthetic_data(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """Generate reproducible, explicitly synthetic poll responses."""
    if n < 1:
        raise ValueError("n must be at least 1")
    rng = np.random.default_rng(seed)
    regions = np.array(["North", "South", "East", "West", "Central"])
    age_groups = np.array(["18-24", "25-34", "35-44", "45+"])
    options = np.array(["Python", "Excel", "Power BI", "Tableau"])
    # Slightly different distributions by region to enable comparison.
    probabilities = {
        "North": [0.42, 0.20, 0.23, 0.15],
        "South": [0.31, 0.24, 0.27, 0.18],
        "East": [0.34, 0.28, 0.20, 0.18],
        "West": [0.36, 0.18, 0.28, 0.18],
        "Central": [0.33, 0.25, 0.24, 0.18],
    }
    chosen_regions = rng.choice(regions, size=n)
    chosen_options = [
        rng.choice(options, p=probabilities[region]) for region in chosen_regions
    ]
    start = pd.Timestamp("2026-09-01")
    offsets = rng.integers(0, 40 * 24 * 60, size=n)
    timestamps = start + pd.to_timedelta(offsets, unit="m")
    return pd.DataFrame({
        "Respondent ID": [f"R{i:04d}" for i in range(1, n + 1)],
        "Timestamp": timestamps,
        "Question": "Which data tool do you prefer?",
        "Option": chosen_options,
        "Region": chosen_regions,
        "Age Group": rng.choice(age_groups, size=n, p=[0.38, 0.32, 0.18, 0.12]),
    })


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate required columns and return a cleaned copy."""
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    cleaned = df.copy()
    for column in ["Question", "Option", "Region", "Age Group"]:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)
    cleaned["Timestamp"] = pd.to_datetime(cleaned["Timestamp"], errors="coerce")
    cleaned = cleaned.dropna(subset=REQUIRED_COLUMNS)
    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned[cleaned["Option"].astype(str).str.len() > 0]
    return cleaned.reset_index(drop=True)


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load and clean a CSV file."""
    return clean_data(pd.read_csv(path))
