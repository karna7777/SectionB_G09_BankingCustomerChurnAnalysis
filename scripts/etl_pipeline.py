"""
ETL pipeline for the Banking Customer Churn Analysis project.

This script reproduces the cleaning steps used in 02_cleaning.ipynb and
creates the final cleaned dataset used by EDA, statistical analysis, KPI
calculation, and Tableau dashboards.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "churn_prediction.csv"
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "churn_clean.csv"


MONEY_COLUMNS = [
    "current_balance",
    "previous_month_end_balance",
    "average_monthly_balance_prevQ",
    "average_monthly_balance_prevQ2",
    "current_month_credit",
    "previous_month_credit",
    "current_month_debit",
    "previous_month_debit",
    "current_month_balance",
    "previous_month_balance",
]


DROP_COLUMNS = ["customer_id", "branch_code", "city"]


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the original customer churn dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    return pd.read_csv(path)


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate customer records if any are present."""
    return df.drop_duplicates().copy()


def drop_non_analytical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop identifier/location fields that are not used in analysis."""
    existing_drop_cols = [col for col in DROP_COLUMNS if col in df.columns]
    return df.drop(columns=existing_drop_cols)


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values using business-appropriate rules."""
    df = df.copy()

    df["gender"] = df["gender"].fillna(df["gender"].mode()[0])
    df["gender"] = df["gender"].replace("Other", df["gender"].mode()[0])
    df["dependents"] = df["dependents"].fillna(df["dependents"].median())
    df["occupation"] = df["occupation"].fillna("Unknown")

    return df


def clean_monetary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Replace negative monetary values and cap extreme outliers."""
    df = df.copy()

    for col in MONEY_COLUMNS:
        df[col] = df[col].clip(lower=0)

    for col in MONEY_COLUMNS:
        lower_limit = df[col].quantile(0.01)
        upper_limit = df[col].quantile(0.99)
        df[col] = df[col].clip(lower=lower_limit, upper=upper_limit)

    return df


def create_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create transaction date fields and a missing transaction flag."""
    df = df.copy()

    df["last_transaction"] = pd.to_datetime(df["last_transaction"], errors="coerce")
    df["transaction_year"] = df["last_transaction"].dt.year
    df["transaction_month"] = df["last_transaction"].dt.month
    df["transaction_day"] = df["last_transaction"].dt.day
    df["no_transaction_flag"] = df["last_transaction"].isna().astype(int)

    return df


def create_business_segments(df: pd.DataFrame) -> pd.DataFrame:
    """Create customer segments for EDA, KPI reporting, and Tableau."""
    df = df.copy()

    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 25, 40, 60, 100],
        labels=["Young", "Adult", "Middle Age", "Senior"],
        include_lowest=True,
    )

    df["balance_segment"] = pd.cut(
        df["current_balance"],
        bins=[-1, 1000, 10000, np.inf],
        labels=["Low", "Medium", "High"],
    )

    df["total_transactions"] = (
        df["current_month_credit"] + df["current_month_debit"]
    )

    df["activity_level"] = pd.cut(
        df["total_transactions"],
        bins=[-1, 1000, 10000, 50000, np.inf],
        labels=["Low Activity", "Moderate", "High", "Very High"],
    )

    return df


def validate_clean_data(df: pd.DataFrame) -> None:
    """Run final quality checks before saving the cleaned dataset."""
    negative_counts = (df[MONEY_COLUMNS] < 0).sum()
    if negative_counts.sum() > 0:
        raise ValueError(f"Negative monetary values found:\n{negative_counts}")

    required_columns = [
        "vintage",
        "age",
        "gender",
        "dependents",
        "occupation",
        "customer_nw_category",
        "current_balance",
        "churn",
        "age_group",
        "balance_segment",
        "total_transactions",
        "activity_level",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required cleaned columns: {missing_columns}")


def run_pipeline() -> pd.DataFrame:
    """Run the full extraction, transformation, and load process."""
    df = load_raw_data()
    initial_shape = df.shape

    df = remove_duplicates(df)
    df = drop_non_analytical_columns(df)
    df = handle_missing_values(df)
    df = clean_monetary_columns(df)
    df = create_date_features(df)
    df = create_business_segments(df)
    validate_clean_data(df)

    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DATA_PATH, index=False)

    churn_rate = df["churn"].mean() * 100
    print("ETL pipeline completed successfully.")
    print(f"Raw shape: {initial_shape}")
    print(f"Clean shape: {df.shape}")
    print(f"Clean file saved to: {CLEAN_DATA_PATH}")
    print(f"Overall churn rate: {churn_rate:.2f}%")

    return df


if __name__ == "__main__":
    run_pipeline()
