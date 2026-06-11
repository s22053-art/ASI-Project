# Przewidywanie satysfakcji z lotu samolotem

Projekt przewiduje, czy pasazer bedzie zadowolony z lotu samolotem. Model
korzysta z danych o pasazerze, typie podrozy, klasie, dystansie lotu, ocenach
uslug oraz opoznieniach.

Target modelu to kolumna `satisfaction`:

- `satisfied`
- `neutral or dissatisfied`

## Co zawiera projekt

```text
data/raw/          train.csv i test.csv
data/processed/    wyniki predykcji batch
models/            zapisany model i metryki
notebooks/         baseline w Jupyter Notebook
src/               kod ML, pipeline i API
web/               strona HTML demo
tests/             testy jednostkowe
docs/              diagram i konspekt prezentacji
```

## Instalacja

W projekcie jest przenosny Python:

```powershell
F:\ASI\tools\Python310\python.exe --version
```

Podstawowe zaleznosci:

```powershell
cd F:\ASI
F:\ASI\tools\Python310\python.exe -m pip install -r requirements.txt
```

Opcjonalne zaleznosci do rozszerzen, takich jak AutoML i monitoring:

```powershell
F:\ASI\tools\Python310\python.exe -m pip install -r requirements-optional.txt
```

## Trening

Najprostsza komenda:

```powershell
cd F:\ASI
F:\ASI\tools\Python310\python.exe -m airline_satisfaction.pipeline train
```

Efekty:

- `models/model.joblib`
- `models/metrics.json`
- `models/reference_profile.json`

Mozna tez uruchomic wersje Kedro:

```powershell
F:\ASI\tools\Python310\python.exe -m kedro run
```

## Strona demo i API

Po wytrenowaniu modelu:

```powershell
cd F:\ASI
F:\ASI\tools\Python310\python.exe -m uvicorn airline_satisfaction.api.main:app --reload
```

Adresy:

- strona demo: `http://127.0.0.1:8000/`
- dokumentacja API: `http://127.0.0.1:8000/docs`
- health check: `http://127.0.0.1:8000/health`

## Predykcja batch

```powershell
F:\ASI\tools\Python310\python.exe -m airline_satisfaction.pipeline predict --input data/raw/test.csv --output data/processed/predictions.csv
```

## Testy

```powershell
F:\ASI\tools\Python310\python.exe -m ruff check src tests scripts
F:\ASI\tools\Python310\python.exe -m pytest
```

## Wersja uproszczona

Do zaliczenia i demo wystarcza glowna sciezka:

1. Notebook baseline w `notebooks/01_baseline.ipynb`.
2. Pipeline treningu w `src/airline_satisfaction/pipeline.py`.
3. Zapisany model w `models/model.joblib`.
4. API FastAPI i strona HTML w `web/`.
5. Testy, Dockerfile i GitHub Actions.

MLflow, PyCaret i Evidently zostaja jako rozszerzenia opcjonalne, opisane w
kodzie i osobnym pliku `requirements-optional.txt`.

## Wyniki modelu

Aktualnie wytrenowany model Random Forest uzyskal na zbiorze testowym:

```text
accuracy: 0.9614
precision: 0.9696
recall: 0.9416
f1: 0.9554
roc_auc: 0.9937
```

## Dokumentacja

- Diagram architektury: `docs/architecture.md`
- Konspekt prezentacji: `docs/presentation_outline.md`
