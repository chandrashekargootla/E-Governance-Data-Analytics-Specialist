"""
Week 2 Task: Data Cleaning and Preprocessing for E-Governance

This script demonstrates a practical data-cleaning workflow using
Pandas and NumPy.

Expected input:
    e_governance_data.csv

Expected output:
    cleaned_e_governance_data.csv

If the input CSV is not available, the script creates a small sample
e-governance dataset so the workflow can still be demonstrated.
"""

import numpy as np
import pandas as pd


INPUT_FILE = "e_governance_data.csv"
OUTPUT_FILE = "cleaned_e_governance_data.csv"


def create_sample_data():
    """Create sample raw e-governance data for demonstration."""
    data = {
        "application_id": [1001, 1002, 1003, 1003, 1004, 1005, 1006],
        "department": [
            " Revenue ",
            "health",
            None,
            None,
            "Education ",
            "Revenue",
            "HEALTH",
        ],
        "date": [
            "2026-01-05",
            "05/01/2026",
            "2026-01-07",
            "2026-01-07",
            "2026-01-08",
            "invalid-date",
            "2026-01-10",
        ],
        "applications": [120, 80, np.nan, np.nan, 150, 100000, 80],
        "processing_time": [4, np.nan, 7, 7, 5, 6, np.nan],
    }
    return pd.DataFrame(data)


def load_data():
    """Load the input CSV, or create sample data if it is unavailable."""
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Loaded dataset: {INPUT_FILE}")
    except FileNotFoundError:
        print(f"{INPUT_FILE} not found. Using sample data for demonstration.")
        df = create_sample_data()

    return df


def clean_data(df):
    """Apply the Week 2 cleaning and preprocessing steps."""
    print("\n--- Initial dataset information ---")
    print(df.info())
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # 1. Standardize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # 2. Clean text fields
    if "department" in df.columns:
        df["department"] = (
            df["department"]
            .astype("string")
            .str.strip()
            .str.title()
            .fillna("Unknown")
        )

    # 3. Convert dates to a consistent datetime format
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 4. Convert likely numerical columns to numeric values
    numeric_columns = ["applications", "processing_time"]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # 5. Remove exact duplicate rows
    duplicate_count = df.duplicated().sum()
    print(f"\nDuplicate rows found: {duplicate_count}")
    df = df.drop_duplicates().copy()

    # 6. Handle missing numerical values using the median
    for column in numeric_columns:
        if column in df.columns:
            df[column] = df[column].fillna(df[column].median())

    # 7. Handle missing categorical values
    if "department" in df.columns:
        df["department"] = df["department"].fillna("Unknown")

    # 8. Detect outliers using the IQR method
    if "applications" in df.columns:
        q1 = df["applications"].quantile(0.25)
        q3 = df["applications"].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        df["is_applications_outlier"] = (
            (df["applications"] < lower_bound)
            | (df["applications"] > upper_bound)
        )

        print(
            f"Applications outlier limits: "
            f"{lower_bound:.2f} to {upper_bound:.2f}"
        )

    # 9. Min-Max normalization
    if "applications" in df.columns:
        min_value = df["applications"].min()
        max_value = df["applications"].max()

        if max_value != min_value:
            df["applications_normalized"] = (
                (df["applications"] - min_value)
                / (max_value - min_value)
            )
        else:
            df["applications_normalized"] = 0.0

    return df


def validate_data(df):
    """Validate the cleaned dataset."""
    print("\n--- Validation after cleaning ---")
    print("Missing values:")
    print(df.isnull().sum())

    print(f"\nDuplicate rows remaining: {df.duplicated().sum()}")

    print("\nData types:")
    print(df.dtypes)

    if "applications_normalized" in df.columns:
        print("\nNormalized applications range:")
        print(
            df["applications_normalized"].min(),
            "to",
            df["applications_normalized"].max(),
        )


def main():
    """Run the complete cleaning workflow."""
    df = load_data()
    cleaned_df = clean_data(df)
    validate_data(cleaned_df)

    cleaned_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nCleaned dataset saved as: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
