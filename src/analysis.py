
import pandas as pd


def get_safety_summary(df: pd.DataFrame) -> dict:
    """Summarize historical airline safety data."""
    required = [
        "airline",
        "incidents_85_99",
        "fatal_accidents_85_99",
        "fatalities_85_99",
        "incidents_00_14",
        "fatal_accidents_00_14",
        "fatalities_00_14",
        "avail_seat_km_per_week",
    ]

    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return {
        "airline_count": int(df["airline"].nunique()),
        "incidents_1985_1999": int(df["incidents_85_99"].sum()),
        "incidents_2000_2014": int(df["incidents_00_14"].sum()),
        "fatal_accidents_1985_1999": int(
            df["fatal_accidents_85_99"].sum()
        ),
        "fatal_accidents_2000_2014": int(
            df["fatal_accidents_00_14"].sum()
        ),
        "fatalities_1985_1999": int(df["fatalities_85_99"].sum()),
        "fatalities_2000_2014": int(df["fatalities_00_14"].sum()),
    }


def compare_periods(df: pd.DataFrame) -> pd.DataFrame:
    """Compare recorded incidents and fatalities by airline."""
    result = df[["airline"]].copy()

    result["Incidents (1985–1999)"] = df["incidents_85_99"]
    result["Incidents (2000–2014)"] = df["incidents_00_14"]
    result["Fatal accidents (1985–1999)"] = df["fatal_accidents_85_99"]
    result["Fatal accidents (2000–2014)"] = df["fatal_accidents_00_14"]
    result["Fatalities (1985–1999)"] = df["fatalities_85_99"]
    result["Fatalities (2000–2014)"] = df["fatalities_00_14"]

    return result


def get_top_airlines(
    df: pd.DataFrame,
    metric: str = "incidents_00_14",
    n: int = 10,
) -> pd.DataFrame:
    """Return airlines sorted by a recorded historical metric."""
    allowed_metrics = {
        "incidents_85_99",
        "fatal_accidents_85_99",
        "fatalities_85_99",
        "incidents_00_14",
        "fatal_accidents_00_14",
        "fatalities_00_14",
    }

    if metric not in allowed_metrics:
        raise ValueError(f"Unsupported metric: {metric}")

    if n < 1:
        raise ValueError("n must be at least 1")

    return (
        df[["airline", metric]]
        .sort_values(metric, ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
