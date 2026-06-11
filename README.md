# Przewidywanie satysfakcji z lotu samolotem

Projekt klasyfikuje, czy pasażer będzie zadowolony z lotu samolotem na podstawie danych demograficznych, typu podróży, klasy, ocen usług oraz opóźnień.

**Target:** kolumna `satisfaction` — `satisfied` / `neutral or dissatisfied`

**Wyniki modelu (Random Forest):**

| Metryka   | Wartość |
|-----------|---------|
| Accuracy  | 96.1%   |
| Precision | 97.0%   |
| Recall    | 94.2%   |
| F1        | 95.5%   |
| ROC-AUC   | 99.4%   |

---

## Struktura projektu

```
ASI-Project/
├── .github/workflows/   # CI/CD — GitHub Actions
├── conf/                # Konfiguracja Kedro
├── data/
│   ├── raw/             # Dane wejściowe (train.csv, test.csv)
│   └── processed/       # Wyniki predykcji batch
├── docs/
│   ├── architecture.md         # Diagram architektury systemu
│   └── presentation_outline.md # Konspekt prezentacji
├── models/              # Zapisany model, metryki, profil referencyjny
├── notebooks/           # Notebook baseline (EDA + trening)
├── src/airline_satisfaction/
│   ├── api/             # FastAPI — endpointy predykcji
│   ├── pipelines/       # Pipeline Kedro
│   ├── data.py          # Ładowanie i walidacja danych
│   ├── features.py      # Inżynieria cech
│   ├── train.py         # Trening i strojenie modelu
│   ├── evaluate.py      # Ewaluacja
│   ├── predict.py       # Predykcja + logowanie
│   ├── drift.py         # Monitoring driftu danych
│   ├── mlflow_tracking.py  # Śledzenie eksperymentów (opcjonalne)
│   └── automl.py        # AutoML PyCaret (opcjonalne)
├── tests/               # Testy jednostkowe (pytest)
├── web/                 # Strona demo HTML
├── Dockerfile
├── requirements.txt
└── requirements-optional.txt
```

---

## Instalacja

**Wymagania:** Python 3.10+

```bash
# Sklonuj repozytorium
git clone https://github.com/s22053-art/ASI-Project.git
cd ASI-Project

# Zainstaluj zależności podstawowe
pip install -r requirements.txt

# Opcjonalnie: MLflow, PyCaret, Evidently
pip install -r requirements-optional.txt
```

---

## Trening modelu

```bash
python -m airline_satisfaction.pipeline train
```

Efekty:
- `models/model.joblib` — wytrenowany model
- `models/metrics.json` — metryki na zbiorze testowym
- `models/reference_profile.json` — profil referencyjny do monitoringu driftu

Alternatywnie przez Kedro:
```bash
kedro run
```

---

## Uruchomienie API i strony demo

```bash
uvicorn airline_satisfaction.api.main:app --reload
```

| Adres | Opis |
|-------|------|
| `http://127.0.0.1:8000/` | Strona demo HTML |
| `http://127.0.0.1:8000/docs` | Dokumentacja Swagger UI |
| `http://127.0.0.1:8000/health` | Health check |
| `http://127.0.0.1:8000/predict` | Endpoint predykcji (POST) |

Każda predykcja jest logowana do `logs/predictions.jsonl`.

---

## Predykcja batch

```bash
python -m airline_satisfaction.pipeline predict \
  --input data/raw/test.csv \
  --output data/processed/predictions.csv
```

---

## Testy

```bash
pytest tests/ -v
```

Linting:
```bash
ruff check src/
```

---

## Docker

```bash
docker build -t airline-satisfaction .
docker run -p 8000:8000 airline-satisfaction
```

---

## Dokumentacja

- [Diagram architektury](docs/architecture.md)
- [Konspekt prezentacji](docs/presentation_outline.md)

---

## Technologie

- **Model:** scikit-learn (Random Forest), strojenie przez RandomizedSearchCV
- **Pipeline:** Kedro
- **API:** FastAPI + Uvicorn
- **Testy:** pytest
- **CI/CD:** GitHub Actions
- **Monitoring:** wykrywanie driftu danych (`drift.py`)
- **Opcjonalnie:** MLflow, PyCaret, Evidently
