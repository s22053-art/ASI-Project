FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY models/ ./models/
COPY web/ ./web/
COPY data/raw/ ./data/raw/
COPY conf/ ./conf/

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "airline_satisfaction.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
