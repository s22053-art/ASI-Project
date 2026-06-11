"""Project configuration constants."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

TRAIN_PATH = RAW_DATA_DIR / "train.csv"
TEST_PATH = RAW_DATA_DIR / "test.csv"
MODEL_PATH = MODELS_DIR / "model.joblib"
METRICS_PATH = MODELS_DIR / "metrics.json"
PREDICTION_LOG_PATH = LOGS_DIR / "predictions.jsonl"
REFERENCE_PROFILE_PATH = MODELS_DIR / "reference_profile.json"

TARGET_COLUMN = "satisfaction"
POSITIVE_LABEL = "satisfied"
NEGATIVE_LABEL = "neutral or dissatisfied"
DROP_COLUMNS = ["Unnamed: 0", "id"]
RANDOM_STATE = 42

CATEGORICAL_COLUMNS = [
    "Gender",
    "Customer Type",
    "Type of Travel",
    "Class",
]

NUMERIC_COLUMNS = [
    "Age",
    "Flight Distance",
    "Inflight wifi service",
    "Departure/Arrival time convenient",
    "Ease of Online booking",
    "Gate location",
    "Food and drink",
    "Online boarding",
    "Seat comfort",
    "Inflight entertainment",
    "On-board service",
    "Leg room service",
    "Baggage handling",
    "Checkin service",
    "Inflight service",
    "Cleanliness",
    "Departure Delay in Minutes",
    "Arrival Delay in Minutes",
]
