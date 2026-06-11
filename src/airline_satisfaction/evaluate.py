"""Model evaluation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_classifier(model: Any, X: pd.DataFrame, y: pd.Series) -> dict[str, Any]:
    """Evaluate a fitted binary classifier."""
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]
    matrix = confusion_matrix(y, y_pred).tolist()

    return {
        "accuracy": float(accuracy_score(y, y_pred)),
        "precision": float(precision_score(y, y_pred)),
        "recall": float(recall_score(y, y_pred)),
        "f1": float(f1_score(y, y_pred)),
        "roc_auc": float(roc_auc_score(y, y_proba)),
        "confusion_matrix": matrix,
    }


def save_metrics(metrics: dict[str, Any], path: Path) -> None:
    """Save metrics as readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
