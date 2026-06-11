# Instrukcja użycia — Airline Satisfaction

## Wymagania

- Python 3.10+
- Anaconda (zalecane) lub pip
- Dane: `train.csv` i `test.csv` (nie są w repozytorium — należy dostarczyć osobno)

---

## Instalacja

```bash
git clone https://github.com/s22053-art/ASI-Project.git
cd ASI-Project

pip install -r requirements.txt
```

Opcjonalne rozszerzenia (MLflow, PyCaret, Evidently):
```bash
pip install -r requirements-optional.txt
```

---

## Dane wejściowe

Skopiuj dane do katalogu projektu:
```bash
mkdir -p data/raw
cp /ścieżka/do/train.csv data/raw/
cp /ścieżka/do/test.csv data/raw/
```

---

## Trening modelu

```bash
PYTHONPATH=src python -m airline_satisfaction.pipeline train
```

Po treningu powstaną pliki:
- `models/model.joblib` — wytrenowany model
- `models/metrics.json` — metryki (accuracy, F1, ROC-AUC itp.)
- `models/reference_profile.json` — profil do monitoringu driftu

Przykładowy wynik treningu:
```json
{
  "accuracy": 0.9614,
  "precision": 0.9696,
  "recall": 0.9416,
  "f1": 0.9554,
  "roc_auc": 0.9937
}
```

---

## Uruchomienie API

```bash
PYTHONPATH=src uvicorn airline_satisfaction.api.main:app --reload
```

Dostępne adresy:
- Strona demo: `http://127.0.0.1:8000/`
- Dokumentacja API: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

---

## Predykcja batch (plik CSV)

Aby przewidzieć satysfakcję dla całego zbioru testowego:

```bash
PYTHONPATH=src python -m airline_satisfaction.pipeline predict \
  --input data/raw/test.csv \
  --output data/processed/predictions.csv
```

Wynik zapisuje się do `data/processed/predictions.csv`.

---

## Testy

```bash
pytest tests/ -v
```

Linting kodu:
```bash
ruff check src/
```

---

## Pipeline Kedro (alternatywa)

```bash
kedro run
```

---

## Docker

```bash
docker build -t airline-satisfaction .
docker run -p 8000:8000 airline-satisfaction
```

Po uruchomieniu API dostępne pod: `http://localhost:8000/`

---

## Struktura katalogów

```
ASI-Project/
├── data/
│   ├── raw/          ← tu wrzucić train.csv i test.csv
│   └── processed/    ← tu trafiają wyniki predykcji
├── models/           ← zapisany model i metryki
├── logs/             ← logi predykcji API (predictions.jsonl)
├── src/              ← kod źródłowy
└── tests/            ← testy jednostkowe
```

---

## Typowe błędy

| Problem | Rozwiązanie |
|---------|-------------|
| `No module named 'airline_satisfaction'` | Dodaj `PYTHONPATH=src` przed komendą |
| `FileNotFoundError: train.csv` | Skopiuj dane do `data/raw/` |
| `Port already in use` | Użyj `--port 8001` lub zatrzymaj inny proces |
