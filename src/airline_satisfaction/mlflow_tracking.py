"""Optional MLflow tracking helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def log_training_run(
    metrics: dict[str, Any],
    model_path: Path,
    experiment_name: str = "airline-satisfaction",
) -> None:
    """Log metrics and model artifact to MLflow when MLflow is installed."""
    try:
        import mlflow
    except ImportError:
        return

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name="sklearn-training"):
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(key, value)
            elif key == "best_params" and isinstance(value, dict):
                mlflow.log_params(value)
            elif key == "model_type":
                mlflow.log_param(key, value)

        if model_path.exists():
            mlflow.log_artifact(str(model_path))
