"""CLI-friendly project pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from airline_satisfaction.predict import batch_predict
from airline_satisfaction.train import train_and_evaluate


def main() -> None:
    """Run training or batch inference from the command line."""
    parser = argparse.ArgumentParser(description="Airline satisfaction ML pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train and evaluate a model")
    train_parser.add_argument(
        "--model-type",
        choices=["random_forest", "logistic_regression"],
        default="random_forest",
    )
    train_parser.add_argument("--tune", action="store_true")
    train_parser.add_argument(
        "--log-mlflow",
        action="store_true",
        help="Log metrics and artifacts to MLflow if optional dependencies exist.",
    )

    predict_parser = subparsers.add_parser("predict", help="Run batch inference")
    predict_parser.add_argument("--input", required=True, type=Path)
    predict_parser.add_argument("--output", required=True, type=Path)

    args = parser.parse_args()

    if args.command == "train":
        metrics = train_and_evaluate(
            model_type=args.model_type,
            tune=args.tune,
            log_mlflow=args.log_mlflow,
        )
        print(json.dumps(metrics, indent=2))
    elif args.command == "predict":
        batch_predict(args.input, args.output)
        print(f"Saved predictions to {args.output}")


if __name__ == "__main__":
    main()
