"""Training entrypoints for baseline and improved models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from airline_satisfaction.config import (
    METRICS_PATH,
    MODEL_PATH,
    RANDOM_STATE,
    REFERENCE_PROFILE_PATH,
)
from airline_satisfaction.data import load_test_data, load_train_data, validate_dataset
from airline_satisfaction.evaluate import evaluate_classifier, save_metrics
from airline_satisfaction.features import (
    add_engineered_features,
    build_preprocessor,
    split_features_target,
)


def build_logistic_regression_pipeline() -> Pipeline:
    """Build a baseline logistic regression pipeline."""
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(use_engineered_features=True)),
            (
                "classifier",
                LogisticRegression(max_iter=1000, class_weight="balanced"),
            ),
        ]
    )


def build_random_forest_pipeline() -> Pipeline:
    """Build a random forest pipeline."""
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(use_engineered_features=True)),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=250,
                    random_state=RANDOM_STATE,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )


def tune_random_forest(X: pd.DataFrame, y: pd.Series) -> RandomizedSearchCV:
    """Tune a random forest model with a compact randomized search."""
    search = RandomizedSearchCV(
        estimator=build_random_forest_pipeline(),
        param_distributions={
            "classifier__n_estimators": [150, 250, 400],
            "classifier__max_depth": [None, 12, 18, 24],
            "classifier__min_samples_split": [2, 5, 10],
            "classifier__min_samples_leaf": [1, 2, 4],
        },
        n_iter=12,
        scoring="f1",
        cv=3,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
    )
    search.fit(X, y)
    return search


def save_model(model: Any, path: Path = MODEL_PATH) -> None:
    """Persist a fitted model pipeline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def save_reference_profile(
    X: pd.DataFrame,
    path: Path = REFERENCE_PROFILE_PATH,
) -> None:
    """Save basic reference statistics for simple drift checks."""
    numeric = X.select_dtypes(include="number")
    profile = {
        column: {
            "mean": float(numeric[column].mean()),
            "std": float(numeric[column].std(ddof=0) or 0.0),
        }
        for column in numeric.columns
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2), encoding="utf-8")


def train_and_evaluate(
    model_type: str = "random_forest",
    tune: bool = False,
    log_mlflow: bool = False,
    model_path: Path = MODEL_PATH,
    metrics_path: Path = METRICS_PATH,
) -> dict[str, Any]:
    """Train, evaluate and persist the selected model."""
    train_df = load_train_data()
    test_df = load_test_data()
    validate_dataset(train_df)
    validate_dataset(test_df)

    train_df = add_engineered_features(train_df)
    test_df = add_engineered_features(test_df)
    X_train, y_train = split_features_target(train_df)
    X_test, y_test = split_features_target(test_df)

    if tune:
        search = tune_random_forest(X_train, y_train)
        model = search.best_estimator_
        params: dict[str, Any] = {"best_params": search.best_params_}
    elif model_type == "logistic_regression":
        model = build_logistic_regression_pipeline()
        model.fit(X_train, y_train)
        params = {"model_type": model_type}
    else:
        model = build_random_forest_pipeline()
        model.fit(X_train, y_train)
        params = {"model_type": "random_forest"}

    metrics = evaluate_classifier(model, X_test, y_test)
    metrics.update(params)

    save_model(model, model_path)
    save_metrics(metrics, metrics_path)
    save_reference_profile(X_train)

    if log_mlflow:
        from airline_satisfaction.mlflow_tracking import log_training_run

        log_training_run(metrics, model_path)

    return metrics


if __name__ == "__main__":
    result = train_and_evaluate()
    print(json.dumps(result, indent=2))
