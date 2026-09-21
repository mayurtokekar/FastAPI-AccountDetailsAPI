# Account Details API

A simple FastAPI service to fetch and manage account details.

## Setup

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If `python` or `py` is not recognized, install Python 3.12 from python.org and ensure the launcher is enabled, or call the full interpreter path directly, for example:

```powershell
& "C:\Users\A\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The log level defaults to `INFO` and can be overridden with the
`LOG_LEVEL` environment variable (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

Then open:
- API root: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Method | Path                  | Description                         |
| ------ | --------------------- | ----------------------------------- |
| GET    | `/`                   | Service status                      |
| GET    | `/health`             | Health check                        |
| GET    | `/accounts`           | List accounts (optional type filter)|
| GET    | `/accounts/{id}`      | Fetch a single account by ID        |
| POST   | `/accounts`           | Create a new account                |

## Example requests

```bash
# List all accounts
curl http://localhost:8000/accounts

# List savings accounts only
curl "http://localhost:8000/accounts?account_type=savings"

# Fetch account 1
curl http://localhost:8000/accounts/1

# Create a new account
curl -X POST http://localhost:8000/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","phone":"+1-555-0199","account_type":"checking"}'
```

## Project layout

```
.
├── main.py             # FastAPI app, routes, request logging middleware
├── models.py           # Pydantic request/response models
├── database.py         # In-memory account store (thread-safe, seeded)
├── logging_config.py   # JSON formatter, level config, helpers
├── requirements.txt
└── README.md
```

The store is in-memory and seeded with three example accounts on startup.
Swap `database.py` for a real database (Postgres, SQLite, etc.) when you're ready.

## Logging

Logs are emitted as one JSON object per line on stdout — easy to ship to
Loki, Datadog, CloudWatch, etc.

Each request gets a `request_id` (taken from the incoming `X-Request-ID`
header, or generated). The same id appears in:

- the `request_id` field of every log line for that request
- the `X-Request-ID` response header
- error response bodies (e.g. `{"error": "...", "request_id": "..."}`)

Example log line:

```json
{"timestamp":"2026-09-21T13:45:00.123456+00:00","level":"INFO","logger":"account_details.api","message":"request.completed","request_id":"a1b2c3...","service":"account-details-api","method":"GET","path":"/accounts/1","status_code":200}
```

Configure with `LOG_LEVEL=DEBUG uvicorn main:app ...` for verbose output.
