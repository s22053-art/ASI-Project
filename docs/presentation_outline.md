# Konspekt prezentacji — Przewidywanie satysfakcji z lotu samolotem

**Czas:** 10–15 minut  
**Zespół:** Kamila Horodenska-Wieczorek & Mateusz Magierski & Michał Nerkowski
**Repozytorium:** [link do GitHub/GitLab]

---

## Slajd 1 — Temat i zespół (1 min)

- Tytuł: „Przewidywanie satysfakcji pasażera linii lotniczej"
- Członkowie zespołu i podział ról
- Link do repozytorium

---

## Slajd 2 — Problem i dane (2 min)

- **Problem:** Linie lotnicze chcą przewidzieć, czy pasażer będzie zadowolony z lotu, zanim otrzymają ankietę
- **Dane:** 103 904 rekordów treningowych, 25 976 testowych
- **Target:** `satisfaction` — dwie klasy: `satisfied` / `neutral or dissatisfied`
- **Cechy:** dane demograficzne, klasa lotu, oceny usług (0–5), opóźnienia
- Krótkie EDA: rozkład targetu, najważniejsze korelacje

---

## Slajd 3 — Inżynieria cech i preprocessing (2 min)

- 4 nowe cechy: `Total Delay`, `Has Delay`, `Delay Ratio`, `Flight Distance Segment`
- Preprocessing pipeline: `StandardScaler` dla numerycznych, `OneHotEncoder` dla kategorycznych, imputacja braków
- Selekcja cech: dlaczego te, a nie inne

---

## Slajd 4 — Modele i wyniki (2 min)

| Model               | Accuracy | F1    | ROC-AUC |
|---------------------|----------|-------|---------|
| Logistic Regression | ~0.87    | ~0.85 | ~0.94   |
| Random Forest       | **0.961**| **0.955** | **0.994** |

- Strojenie hiperparametrów: `RandomizedSearchCV` (12 iteracji, cv=3)
- Najlepszy model: Random Forest z 250 drzewami
- AutoML (PyCaret): potwierdzenie wyboru Random Forest

---

## Slajd 5 — Architektura systemu (2 min)

- Diagram z `docs/architecture.md`
- Przepływ danych: CSV → Pipeline ML → model.joblib → FastAPI → klient
- Kedro Pipeline: `kedro run` uruchamia cały flow
- Śledzenie eksperymentów: MLflow (opcjonalne)

---

## Slajd 6 — Pipeline produkcyjny i MLOps (2 min)

- **FastAPI:** endpointy `/predict`, `/health`, `/docs`
- **Logowanie predykcji:** każda predykcja zapisywana do `logs/predictions.jsonl`
- **Monitoring driftu:** `drift.py` porównuje dane wejściowe z profilem referencyjnym
- **Docker:** `Dockerfile` do konteneryzacji
- **CI/CD:** GitHub Actions — testy i linting przy każdym pushu

---

## Slajd 7 — Demo (2 min)

Demonstracja na żywo:
1. Uruchomienie API: `uvicorn airline_satisfaction.api.main:app --reload`
2. Otwarcie strony demo: `http://127.0.0.1:8000/`
3. Wypełnienie formularza i predykcja
4. Swagger UI: `http://127.0.0.1:8000/docs`
5. Uruchomienie testów: `pytest tests/ -v`

---

## Slajd 8 — Podsumowanie i wnioski (1 min)

- Model osiąga 96% accuracy i 99.4% ROC-AUC
- Najważniejsze cechy: `Online boarding`, `Inflight entertainment`, `Class`
- Co można ulepszyć: XGBoost, więcej inżynierii cech, Evidently dashboard
- Pytania?

---

## Notatki dla prezentujących

- Przed prezentacją: uruchomić API i sprawdzić czy działa (`/health`)
- Mieć otwarty notebook z outputami jako backup
- Czas demo to max 2 minuty — nie wnikać w szczegóły kodu
