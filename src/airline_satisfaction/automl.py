"""PyCaret AutoML experiment helper."""

from __future__ import annotations

from airline_satisfaction.data import load_train_data
from airline_satisfaction.features import add_engineered_features


def run_pycaret_automl():
    """Run a compact PyCaret classification comparison."""
    try:
        from pycaret.classification import compare_models, pull, setup
    except ImportError as exc:
        raise RuntimeError("Install pycaret to run AutoML experiments.") from exc

    data = add_engineered_features(load_train_data())
    setup(
        data=data,
        target="satisfaction",
        ignore_features=["Unnamed: 0", "id"],
        session_id=42,
        verbose=False,
    )
    best_model = compare_models(sort="F1")
    leaderboard = pull()
    return best_model, leaderboard


if __name__ == "__main__":
    model, results = run_pycaret_automl()
    print(model)
    print(results.head(10).to_string())
