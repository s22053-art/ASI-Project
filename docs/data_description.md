# Opis danych — Airline Satisfaction

## Źródło

Dane pochodzą z publicznie dostępnego zbioru dotyczącego satysfakcji pasażerów linii lotniczych (Kaggle: *Airline Passenger Satisfaction*).

## Pliki

| Plik | Rozmiar | Opis |
|------|---------|------|
| `data/raw/train.csv` | ~96 000 wierszy | Zbiór treningowy |
| `data/raw/test.csv` | ~26 000 wierszy | Zbiór testowy |

---

## Zmienna docelowa

| Kolumna | Typ | Wartości |
|---------|-----|----------|
| `satisfaction` | string | `satisfied`, `neutral or dissatisfied` |

Rozkład klas w zbiorze treningowym jest zbliżony do 50/50.

---

## Opis kolumn

### Dane demograficzne i podróży

| Kolumna | Typ | Opis | Przykładowe wartości |
|---------|-----|------|----------------------|
| `Gender` | string | Płeć pasażera | `Male`, `Female` |
| `Customer Type` | string | Typ klienta | `Loyal Customer`, `disloyal Customer` |
| `Age` | int | Wiek pasażera | 7–85 |
| `Type of Travel` | string | Cel podróży | `Business travel`, `Personal Travel` |
| `Class` | string | Klasa lotu | `Business`, `Eco`, `Eco Plus` |
| `Flight Distance` | int | Dystans lotu (mile) | 31–4983 |

### Oceny usług (skala 0–5)

Pasażer ocenia każdą usługę w skali od 0 (brak oceny) do 5 (najwyższa ocena).

| Kolumna | Opis |
|---------|------|
| `Inflight wifi service` | Jakość Wi-Fi na pokładzie |
| `Departure/Arrival time convenient` | Wygoda godzin odlotu/przylotu |
| `Ease of Online booking` | Łatwość rezerwacji online |
| `Gate location` | Lokalizacja bramki |
| `Food and drink` | Jedzenie i napoje |
| `Online boarding` | Odprawy online |
| `Seat comfort` | Komfort siedzenia |
| `Inflight entertainment` | Rozrywka na pokładzie |
| `On-board service` | Obsługa na pokładzie |
| `Leg room service` | Przestrzeń na nogi |
| `Baggage handling` | Obsługa bagażu |
| `Checkin service` | Obsługa odprawy |
| `Inflight service` | Obsługa w trakcie lotu |
| `Cleanliness` | Czystość |

### Opóźnienia

| Kolumna | Typ | Opis |
|---------|-----|------|
| `Departure Delay in Minutes` | int | Opóźnienie odlotu (minuty) |
| `Arrival Delay in Minutes` | float | Opóźnienie przylotu (minuty), może zawierać braki |

---

## Przetwarzanie danych

Pipeline wykonuje następujące kroki:

1. **Usunięcie braków** — wiersze z brakującymi wartościami w `Arrival Delay in Minutes` są usuwane (ok. 0.3% danych).
2. **Kodowanie zmiennych kategorycznych** — `Gender`, `Customer Type`, `Type of Travel`, `Class` są kodowane binarnie (Label Encoding).
3. **Brak normalizacji** — Random Forest nie wymaga skalowania cech.

---

## Najważniejsze cechy (Feature Importance)

Na podstawie modelu Random Forest, najsilniejszy wpływ na predykcję mają:

1. `Online boarding` — ocena odpraw online
2. `Inflight entertainment` — rozrywka na pokładzie
3. `Seat comfort` — komfort siedzenia
4. `Class` — klasa lotu (Business vs Eco)
5. `Type of Travel` — cel podróży (biznes vs prywatny)

Pasażerowie podróżujący w klasie biznesowej w celach służbowych są zdecydowanie bardziej skłonni do bycia zadowolonymi.

---

## Statystyki

| Metryka | Wartość |
|---------|---------|
| Łączna liczba rekordów | ~129 000 |
| Liczba cech wejściowych | 22 |
| Udział klasy `satisfied` | ~54% |
| Brakujące wartości | ~0.3% (tylko `Arrival Delay`) |
