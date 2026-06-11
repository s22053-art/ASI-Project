"""Simple drift checks for production demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from airline_satisfaction.config import REFERENCE_PROFILE_PATH


def load_reference_profile(path: Path = REFERENCE_PROFILE_PATH) -> dict[str, Any]:
    """Load saved reference statistics."""
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def detect_numeric_drift(
    current: pd.DataFrame,
    reference_path: Path = REFERENCE_PROFILE_PATH,
    z_threshold: float = 3.0,
) -> dict[str, Any]:
    """Detect large mean shifts against saved training statistics."""
    reference = load_reference_profile(reference_path)
    if not reference:
        return {"status": "reference_missing", "drifted_features": []}

    numeric = current.select_dtypes(include="number")
    drifted: list[dict[str, Any]] = []

    for column, stats in reference.items():
        if column not in numeric.columns:
            continue

        reference_std = float(stats.get("std", 0.0))
        if reference_std == 0:
            continue

        current_mean = float(numeric[column].mean())
        z_score = abs(current_mean - float(stats["mean"])) / reference_std
        if z_score >= z_threshold:
            drifted.append(
                {
                    "feature": column,
                    "reference_mean": float(stats["mean"]),
                    "current_mean": current_mean,
                    "z_score": z_score,
                }
            )

    return {
        "status": "drift_detected" if drifted else "ok",
        "drifted_features": drifted,
    }
