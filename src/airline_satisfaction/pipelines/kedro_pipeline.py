"""Kedro-compatible wrapper around the project pipeline.

The project can be run without Kedro through
``python -m airline_satisfaction.pipeline``. This file keeps the required Kedro
integration small and easy to inspect.
"""

from __future__ import annotations

from typing import Any

from airline_satisfaction.train import train_and_evaluate


def train_model_node() -> dict[str, Any]:
    """Kedro node: train and evaluate the default model."""
    return train_and_evaluate(model_type="random_forest", tune=False, log_mlflow=False)


def create_pipeline():
    """Create the Kedro pipeline if Kedro is installed."""
    try:
        from kedro.pipeline import Pipeline, node
    except ImportError as exc:
        raise RuntimeError("Install kedro to use the Kedro pipeline.") from exc

    return Pipeline(
        [
            node(
                func=train_model_node,
                inputs=None,
                outputs="metrics",
                name="train_model_node",
            )
        ]
    )
