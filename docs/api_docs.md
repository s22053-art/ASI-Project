# Dokumentacja API — Airline Satisfaction

API zbudowane w FastAPI umożliwia predykcję satysfakcji pasażera na podstawie danych o podróży.

## Uruchomienie

```bash
PYTHONPATH=src uvicorn airline_satisfaction.api.main:app --reload
```

| Adres | Opis |
|-------|------|
| `http://127.0.0.1:8000/` | Strona demo HTML |
| `http://127.0.0.1:8000/docs` | Interaktywna dokumentacja Swagger UI |
| `http://127.0.0.1:8000/redoc` | Dokumentacja ReDoc |
| `http://127.0.0.1:8000/health` | Health check |
| `http://127.0.0.1:8000/predict` | Endpoint predykcji (POST) |

---

## Endpointy

### GET /health

Sprawdza czy serwis działa.

**Odpowiedź:**
```json
{
  "status": "ok"
}
```

---

### POST /predict

Zwraca predykcję satysfakcji pasażera.

**Nagłówki:**
```
Content-Type: application/json
```

**Ciało żądania (JSON):**

```json
{
  "Gender": "Male",
  "Customer Type": "Loyal Customer",
  "Age": 35,
  "Type of Travel": "Business travel",
  "Class": "Business",
  "Flight Distance": 1200,
  "Inflight wifi service": 4,
  "Departure/Arrival time convenient": 3,
  "Ease of Online booking": 4,
  "Gate location": 3,
  "Food and drink": 4,
  "Online boarding": 5,
  "Seat comfort": 4,
  "Inflight entertainment": 4,
  "On-board service": 4,
  "Leg room service": 3,
  "Baggage handling": 4,
  "Checkin service": 4,
  "Inflight service": 4,
  "Cleanliness": 4,
  "Departure Delay in Minutes": 0,
  "Arrival Delay in Minutes": 0.0
}
```

**Odpowiedź:**
```json
{
  "prediction": "satisfied",
  "probability": 0.94
}
```

**Możliwe wartości `prediction`:**
- `"satisfied"` — pasażer zadowolony
- `"neutral or dissatisfied"` — pasażer niezadowolony lub neutralny

---

### Przykład wywołania (curl)

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Male",
    "Customer Type": "Loyal Customer",
    "Age": 35,
    "Type of Travel": "Business travel",
    "Class": "Business",
    "Flight Distance": 1200,
    "Inflight wifi service": 4,
    "Departure/Arrival time convenient": 3,
    "Ease of Online booking": 4,
    "Gate location": 3,
    "Food and drink": 4,
    "Online boarding": 5,
    "Seat comfort": 4,
    "Inflight entertainment": 4,
    "On-board service": 4,
    "Leg room service": 3,
    "Baggage handling": 4,
    "Checkin service": 4,
    "Inflight service": 4,
    "Cleanliness": 4,
    "Departure Delay in Minutes": 0,
    "Arrival Delay in Minutes": 0.0
  }'
```

### Przykład w Pythonie

```python
import requests

data = {
    "Gender": "Female",
    "Customer Type": "Loyal Customer",
    "Age": 28,
    "Type of Travel": "Business travel",
    "Class": "Business",
    "Flight Distance": 800,
    "Inflight wifi service": 5,
    "Departure/Arrival time convenient": 4,
    "Ease of Online booking": 5,
    "Gate location": 4,
    "Food and drink": 5,
    "Online boarding": 5,
    "Seat comfort": 5,
    "Inflight entertainment": 5,
    "On-board service": 5,
    "Leg room service": 4,
    "Baggage handling": 5,
    "Checkin service": 5,
    "Inflight service": 5,
    "Cleanliness": 5,
    "Departure Delay in Minutes": 0,
    "Arrival Delay in Minutes": 0.0
}

response = requests.post("http://127.0.0.1:8000/predict", json=data)
print(response.json())
```

---

## Logowanie predykcji

Każde zapytanie do `/predict` jest automatycznie logowane do pliku `logs/predictions.jsonl` w formacie JSON Lines. Przykładowy wpis:

```json
{"timestamp": "2026-06-11T20:00:00", "input": {...}, "prediction": "satisfied", "probability": 0.94}
```
