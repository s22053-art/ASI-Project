"""Prediction and batch inference helpers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from airline_satisfaction.config import (
    MODEL_PATH,
    NEGATIVE_LABEL,
    POSITIVE_LABEL,
    PREDICTION_LOG_PATH,
)
from airline_satisfaction.features import add_engineered_features


def load_model(path: Path = MODEL_PATH) -> Any:
    """Load a persisted sklearn pipeline."""
    if not path.exists():
        raise FileNotFoundError(
            f"Model file not found at {path}. Run training before prediction."
        )
    return joblib.load(path)


def predict_dataframe(model: Any, df: pd.DataFrame) -> pd.DataFrame:
    """Predict satisfaction labels and probabilities for a dataframe."""
    features = add_engineered_features(df)
    probabilities = model.predict_proba(features)[:, 1]
    labels = [
        POSITIVE_LABEL if probability >= 0.5 else NEGATIVE_LABEL
        for probability in probabilities
    ]
    return pd.DataFrame(
        {
            "prediction": labels,
            "probability_satisfied": probabilities,
        }
    )


def predict_one(model: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """Predict one passenger satisfaction outcome."""
    prediction = predict_dataframe(model, pd.DataFrame([payload])).iloc[0]
    probability = float(prediction["probability_satisfied"])
    label = str(prediction["prediction"])
    return {
        "prediction": label,
        "probability_satisfied": probability,
        "probability_neutral_or_dissatisfied": 1.0 - probability,
        "interpretation": build_interpretation(label, probability),
    }


def build_interpretation(label: str, probability: float) -> str:
    """Create a short human-readable prediction explanation."""
    confidence = max(probability, 1.0 - probability)
    if label == POSITIVE_LABEL:
        return f"Model przewiduje satysfakcje z pewnoscia {confidence:.1%}."
    return f"Model przewiduje brak satysfakcji z pewnoscia {confidence:.1%}."


def append_prediction_log(
    payload: dict[str, Any],
    prediction: dict[str, Any],
    path: Path = PREDICTION_LOG_PATH,
) -> None:
    """Append a prediction event to a JSONL log."""
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": payload,
        "output": prediction,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")


def batch_predict(
    input_path: Path,
    output_path: Path,
    model_path: Path = MODEL_PATH,
) -> None:
    """Run batch inference from a CSV file to a CSV file."""
    model = load_model(model_path)
    data = pd.read_csv(input_path)
    predictions = predict_dataframe(model, data)
    output = pd.concat([data, predictions], axis=1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)
