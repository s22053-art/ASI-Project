"""Data loading and validation helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from airline_satisfaction.config import (
    RAW_DATA_DIR,
    TARGET_COLUMN,
    TEST_PATH,
    TRAIN_PATH,
)


def load_train_data(path: Path = TRAIN_PATH) -> pd.DataFrame:
    """Load the training dataset."""
    return pd.read_csv(path)


def load_test_data(path: Path = TEST_PATH) -> pd.DataFrame:
    """Load the test dataset."""
    return pd.read_csv(path)


def load_raw_data(data_dir: Path = RAW_DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load train and test CSV files from the raw data directory."""
    return (
        load_train_data(data_dir / "train.csv"),
        load_test_data(data_dir / "test.csv"),
    )


def validate_dataset(df: pd.DataFrame) -> None:
    """Validate the minimum schema expected by the project."""
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    if df.empty:
        raise ValueError("Dataset is empty")
