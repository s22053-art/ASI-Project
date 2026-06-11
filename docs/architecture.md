# Architektura systemu — Przewidywanie satysfakcji z lotu samolotem

## Diagram architektury

```
┌─────────────────────────────────────────────────────────────────┐
│                        DANE WEJŚCIOWE                           │
│   data/raw/train.csv          data/raw/test.csv                 │
└───────────────────┬─────────────────────────┬───────────────────┘
                    │                         │
                    ▼                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE ML  (src/)                          │
│                                                                 │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────────────┐  │
│  │  data.py    │──▶│  features.py │──▶│     train.py        │  │
│  │             │   │              │   │                     │  │
│  │ load_train  │   │ add_engin-   │   │ build_random_forest  │  │
│  │ load_test   │   │ eered_feat.  │   │ tune_random_forest   │  │
│  │ validate    │   │ build_pre-   │   │ train_and_evaluate   │  │
│  │             │   │ processor    │   │                     │  │
│  └─────────────┘   └──────────────┘   └──────────┬──────────┘  │
│                                                  │             │
│  ┌─────────────┐   ┌──────────────┐              │             │
│  │ evaluate.py │◀──│  predict.py  │◀─────────────┘             │
│  │             │   │              │                             │
│  │ accuracy    │   │ predict_one  │                             │
│  │ precision   │   │ batch_pred.  │                             │
│  │ recall, f1  │   │ pred_log     │                             │
│  │ roc_auc     │   │              │                             │
│  └─────────────┘   └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────────────────────────────────┐
│  models/        │  │           OPCJONALNE ROZSZERZENIA            │
│                 │  │                                             │
│ model.joblib    │  │  mlflow_tracking.py  → MLflow Tracking      │
│ metrics.json    │  │  automl.py           → PyCaret AutoML        │
│ reference_      │  │  drift.py            → Evidently monitoring  │
│ profile.json    │  │                                             │
└─────────────────┘  └─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WARSTWA PRODUKCYJNA                         │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   FastAPI  (api/main.py)                  │  │
│  │                                                           │  │
│  │   GET  /          → strona demo HTML (web/)               │  │
│  │   GET  /health    → status serwisu                        │  │
│  │   POST /predict   → predykcja + drift check + log         │  │
│  │   GET  /docs      → dokumentacja Swagger UI               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────┐    ┌──────────────────────────────┐   │
│  │   web/index.html     │    │   logs/predictions.jsonl     │   │
│  │   web/static/app.js  │    │   (logowanie predykcji)      │   │
│  │   web/static/styles  │    └──────────────────────────────┘   │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUKTURA                             │
│                                                                 │
│   Dockerfile          → konteneryzacja aplikacji               │
│   .github/workflows/  → CI/CD (testy, linting przy pushu)      │
│   pyproject.toml      → konfiguracja projektu i pytest         │
│   requirements.txt    → zależności podstawowe                  │
│   requirements-optional.txt → MLflow, PyCaret, Evidently       │
└─────────────────────────────────────────────────────────────────┘
```

## Opis komponentów

### Dane
Zbiór danych zawiera informacje o pasażerach linii lotniczych: dane demograficzne, typ podróży, klasa, oceny usług (skala 0–5) oraz opóźnienia. Target to kolumna `satisfaction` (satisfied / neutral or dissatisfied).

### Inżynieria cech (`features.py`)
Tworzone są 4 nowe cechy na podstawie istniejących:
- `Total Delay in Minutes` — suma opóźnienia odlotu i przylotu
- `Has Delay` — flaga binarna (0/1)
- `Delay Ratio` — stosunek opóźnienia do długości lotu
- `Flight Distance Segment` — kategoryzacja dystansu (short / medium / long / very_long)

### Model
Random Forest Classifier z 250 drzewami, trenowany przez sklearn Pipeline (preprocessing + klasyfikator). Dostępne jest też strojenie hiperparametrów przez `RandomizedSearchCV`.

### API
FastAPI serwuje predykcje w trybie real-time. Każda predykcja jest logowana do `logs/predictions.jsonl` i sprawdzana pod kątem driftu danych względem profilu referencyjnego z treningu.

### Kedro Pipeline
Projekt integruje się z Kedro przez `pipelines/kedro_pipeline.py` i `conf/base/catalog.yml`, umożliwiając uruchomienie przez `kedro run`.
