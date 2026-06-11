"""FastAPI app serving predictions and the HTML demo."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from airline_satisfaction.config import PROJECT_ROOT
from airline_satisfaction.drift import detect_numeric_drift
from airline_satisfaction.predict import (
    append_prediction_log,
    load_model,
    predict_one,
)

WEB_DIR = PROJECT_ROOT / "web"
STATIC_DIR = WEB_DIR / "static"

app = FastAPI(
    title="Przewidywanie satysfakcji z lotu samolotem",
    description="API i strona demo dla modelu klasyfikacji satysfakcji pasazera.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class PassengerInput(BaseModel):
    """Passenger and flight attributes used by the model."""

    gender: Literal["Male", "Female"] = Field(alias="Gender")
    customer_type: Literal["Loyal Customer", "disloyal Customer"] = Field(
        alias="Customer Type"
    )
    age: int = Field(alias="Age", ge=0, le=120)
    type_of_travel: Literal["Business travel", "Personal Travel"] = Field(
        alias="Type of Travel"
    )
    travel_class: Literal["Business", "Eco", "Eco Plus"] = Field(alias="Class")
    flight_distance: int = Field(alias="Flight Distance", ge=0)
    inflight_wifi_service: int = Field(alias="Inflight wifi service", ge=0, le=5)
    departure_arrival_time_convenient: int = Field(
        alias="Departure/Arrival time convenient", ge=0, le=5
    )
    ease_of_online_booking: int = Field(alias="Ease of Online booking", ge=0, le=5)
    gate_location: int = Field(alias="Gate location", ge=0, le=5)
    food_and_drink: int = Field(alias="Food and drink", ge=0, le=5)
    online_boarding: int = Field(alias="Online boarding", ge=0, le=5)
    seat_comfort: int = Field(alias="Seat comfort", ge=0, le=5)
    inflight_entertainment: int = Field(alias="Inflight entertainment", ge=0, le=5)
    on_board_service: int = Field(alias="On-board service", ge=0, le=5)
    leg_room_service: int = Field(alias="Leg room service", ge=0, le=5)
    baggage_handling: int = Field(alias="Baggage handling", ge=0, le=5)
    checkin_service: int = Field(alias="Checkin service", ge=0, le=5)
    inflight_service: int = Field(alias="Inflight service", ge=0, le=5)
    cleanliness: int = Field(alias="Cleanliness", ge=0, le=5)
    departure_delay: int = Field(alias="Departure Delay in Minutes", ge=0)
    arrival_delay: float = Field(alias="Arrival Delay in Minutes", ge=0)

    model_config = {"populate_by_name": True}


@lru_cache(maxsize=1)
def get_model():
    """Load the model once per API process."""
    return load_model()


@app.get("/")
def index() -> FileResponse:
    """Serve the HTML demo."""
    return FileResponse(WEB_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: PassengerInput) -> dict[str, object]:
    """Return a satisfaction prediction for one passenger."""
    if hasattr(payload, "model_dump"):
        data = payload.model_dump(by_alias=True)
    else:
        data = payload.dict(by_alias=True)

    try:
        model = get_model()
        prediction = predict_one(model, data)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    drift = detect_numeric_drift(pd.DataFrame([data]))
    append_prediction_log(data, prediction)
    return {"input": data, "prediction": prediction, "drift": drift}
