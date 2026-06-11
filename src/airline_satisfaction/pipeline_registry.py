"""Kedro pipeline registry."""

from __future__ import annotations

from kedro.pipeline import Pipeline

from airline_satisfaction.pipelines.kedro_pipeline import create_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register project pipelines for Kedro."""
    pipeline = create_pipeline()
    return {
        "__default__": pipeline,
        "training": pipeline,
    }
