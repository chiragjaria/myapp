FROM python:3.10-slim

# needed by psycopg2-binary at runtime
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

---

**3. `requirements.txt` — Good, no changes needed**
```
fastapi
uvicorn
psycopg2-binary
