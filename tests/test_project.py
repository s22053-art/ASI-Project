"""Testy jednostkowe projektu airline_satisfaction."""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

# Dodaj src/ do ścieżki, żeby importy działały bez instalacji pakietu
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from airline_satisfaction.data import validate_dataset
from airline_satisfaction.drift import detect_numeric_drift
from airline_satisfaction.features import (
    add_engineered_features,
    build_preprocessor,
    split_features_target,
)


# ---------------------------------------------------------------------------
# Dane pomocnicze
# ---------------------------------------------------------------------------

def make_sample_df(n: int = 10) -> pd.DataFrame:
    """Zwraca minimalny DataFrame imitujący dane lotnicze."""
    return pd.DataFrame(
        {
            "satisfaction": ["satisfied"] * (n // 2) + ["neutral or dissatisfied"] * (n - n // 2),
            "Gender": ["Male"] * n,
            "Customer Type": ["Loyal Customer"] * n,
            "Age": [30] * n,
            "Type of Travel": ["Business travel"] * n,
            "Class": ["Business"] * n,
            "Flight Distance": [1000] * n,
            "Inflight wifi service": [3] * n,
            "Departure/Arrival time convenient": [3] * n,
            "Ease of Online booking": [3] * n,
            "Gate location": [3] * n,
            "Food and drink": [3] * n,
            "Online boarding": [4] * n,
            "Seat comfort": [4] * n,
            "Inflight entertainment": [4] * n,
            "On-board service": [4] * n,
            "Leg room service": [3] * n,
            "Baggage handling": [4] * n,
            "Checkin service": [4] * n,
            "Inflight service": [4] * n,
            "Cleanliness": [4] * n,
            "Departure Delay in Minutes": [0] * n,
            "Arrival Delay in Minutes": [0.0] * n,
        }
    )


# ---------------------------------------------------------------------------
# Testy: inżynieria cech
# ---------------------------------------------------------------------------

class TestAddEngineeredFeatures:
    def test_adds_total_delay_column(self):
        df = make_sample_df()
        result = add_engineered_features(df)
        assert "Total Delay in Minutes" in result.columns

    def test_adds_has_delay_column(self):
        df = make_sample_df()
        result = add_engineered_features(df)
        assert "Has Delay" in result.columns

    def test_adds_delay_ratio_column(self):
        df = make_sample_df()
        result = add_engineered_features(df)
        assert "Delay Ratio" in result.columns

    def test_adds_flight_distance_segment_column(self):
        df = make_sample_df()
        result = add_engineered_features(df)
        assert "Flight Distance Segment" in result.columns

    def test_total_delay_is_sum_of_departure_and_arrival(self):
        df = make_sample_df()
        df["Departure Delay in Minutes"] = 10
        df["Arrival Delay in Minutes"] = 5.0
        result = add_engineered_features(df)
        assert (result["Total Delay in Minutes"] == 15).all()

    def test_has_delay_is_zero_when_no_delay(self):
        df = make_sample_df()
        result = add_engineered_features(df)
        assert (result["Has Delay"] == 0).all()

    def test_has_delay_is_one_when_delayed(self):
        df = make_sample_df()
        df["Departure Delay in Minutes"] = 20
        result = add_engineered_features(df)
        assert (result["Has Delay"] == 1).all()

    def test_short_flight_segment_label(self):
        df = make_sample_df()
        df["Flight Distance"] = 300
        result = add_engineered_features(df)
        assert (result["Flight Distance Segment"] == "short").all()

    def test_does_not_modify_original_dataframe(self):
        df = make_sample_df()
        original_columns = set(df.columns)
        add_engineered_features(df)
        assert set(df.columns) == original_columns


# ---------------------------------------------------------------------------
# Testy: podział na cechy i target
# ---------------------------------------------------------------------------

class TestSplitFeaturesTarget:
    def test_target_column_not_in_X(self):
        df = add_engineered_features(make_sample_df())
        X, y = split_features_target(df)
        assert "satisfaction" not in X.columns

    def test_y_is_binary(self):
        df = add_engineered_features(make_sample_df())
        _, y = split_features_target(df)
        assert set(y.unique()).issubset({0, 1})

    def test_X_and_y_same_length(self):
        df = add_engineered_features(make_sample_df())
        X, y = split_features_target(df)
        assert len(X) == len(y)

    def test_raises_on_unknown_label(self):
        df = make_sample_df()
        df["satisfaction"] = "unknown_label"
        df = add_engineered_features(df)
        with pytest.raises(ValueError, match="Unknown target labels"):
            split_features_target(df)


# ---------------------------------------------------------------------------
# Testy: walidacja danych
# ---------------------------------------------------------------------------

class TestValidateDataset:
    def test_passes_for_valid_dataframe(self):
        df = make_sample_df()
        validate_dataset(df)  # nie powinno rzucić wyjątku

    def test_raises_when_target_column_missing(self):
        df = make_sample_df().drop(columns=["satisfaction"])
        with pytest.raises(ValueError, match="Missing target column"):
            validate_dataset(df)

    def test_raises_for_empty_dataframe(self):
        df = pd.DataFrame({"satisfaction": []})
        with pytest.raises(ValueError, match="empty"):
            validate_dataset(df)


# ---------------------------------------------------------------------------
# Testy: preprocessor
# ---------------------------------------------------------------------------

class TestBuildPreprocessor:
    def test_preprocessor_fits_and_transforms(self):
        df = add_engineered_features(make_sample_df())
        X, _ = split_features_target(df)
        preprocessor = build_preprocessor(use_engineered_features=True)
        result = preprocessor.fit_transform(X)
        assert result.shape[0] == len(X)

    def test_preprocessor_without_engineered_features(self):
        df = make_sample_df()
        X, _ = split_features_target(df)
        preprocessor = build_preprocessor(use_engineered_features=False)
        result = preprocessor.fit_transform(X)
        assert result.shape[0] == len(X)


# ---------------------------------------------------------------------------
# Testy: wykrywanie driftu
# ---------------------------------------------------------------------------

class TestDetectNumericDrift:
    def test_returns_ok_when_no_reference(self, tmp_path):
        df = make_sample_df()
        result = detect_numeric_drift(df, reference_path=tmp_path / "missing.json")
        assert result["status"] == "reference_missing"

    def test_returns_ok_when_data_matches_reference(self, tmp_path):
        ref = {"Age": {"mean": 30.0, "std": 1.0}}
        ref_path = tmp_path / "reference_profile.json"
        ref_path.write_text(json.dumps(ref))
        df = make_sample_df()
        result = detect_numeric_drift(df, reference_path=ref_path)
        assert result["status"] == "ok"

    def test_detects_drift_on_large_mean_shift(self, tmp_path):
        ref = {"Age": {"mean": 30.0, "std": 1.0}}
        ref_path = tmp_path / "reference_profile.json"
        ref_path.write_text(json.dumps(ref))
        df = make_sample_df()
        df["Age"] = 100  # duże odchylenie od referencji
        result = detect_numeric_drift(df, reference_path=ref_path)
        assert result["status"] == "drift_detected"
        assert any(f["feature"] == "Age" for f in result["drifted_features"])
