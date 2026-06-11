"""Feature engineering and preprocessing utilities."""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from airline_satisfaction.config import (
    CATEGORICAL_COLUMNS,
    DROP_COLUMNS,
    NEGATIVE_LABEL,
    NUMERIC_COLUMNS,
    POSITIVE_LABEL,
    TARGET_COLUMN,
)


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Split dataframe into model features and binary target."""
    data = df.copy()
    y = data[TARGET_COLUMN].map({NEGATIVE_LABEL: 0, POSITIVE_LABEL: 1})

    if y.isna().any():
        unknown = sorted(data.loc[y.isna(), TARGET_COLUMN].dropna().unique())
        raise ValueError(f"Unknown target labels: {unknown}")

    X = data.drop(columns=[TARGET_COLUMN, *DROP_COLUMNS], errors="ignore")
    return X, y.astype(int)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add simple business features used by the improved model."""
    data = df.copy()

    departure_delay = data["Departure Delay in Minutes"].fillna(0)
    arrival_delay = data["Arrival Delay in Minutes"].fillna(0)

    data["Total Delay in Minutes"] = departure_delay + arrival_delay
    data["Has Delay"] = (data["Total Delay in Minutes"] > 0).astype(int)
    data["Delay Ratio"] = data["Total Delay in Minutes"] / (
        data["Flight Distance"].fillna(0) + 1
    )

    data["Flight Distance Segment"] = pd.cut(
        data["Flight Distance"],
        bins=[-1, 500, 1500, 3000, float("inf")],
        labels=["short", "medium", "long", "very_long"],
    ).astype("object")

    return data


def build_preprocessor(use_engineered_features: bool = True) -> ColumnTransformer:
    """Build a sklearn preprocessor for numeric and categorical columns."""
    numeric_columns = NUMERIC_COLUMNS.copy()
    categorical_columns = CATEGORICAL_COLUMNS.copy()

    if use_engineered_features:
        numeric_columns.extend(
            ["Total Delay in Minutes", "Has Delay", "Delay Ratio"]
        )
        categorical_columns.append("Flight Distance Segment")

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_columns),
            ("cat", categorical_pipeline, categorical_columns),
        ]
    )
