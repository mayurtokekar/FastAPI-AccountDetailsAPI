# Account Details API

A simple FastAPI service to fetch and manage account details.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

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
├── main.py          # FastAPI app and routes
├── models.py        # Pydantic request/response models
├── database.py      # In-memory account store (thread-safe, seeded)
├── requirements.txt
└── README.md
```

The store is in-memory and seeded with three example accounts on startup.
Swap `database.py` for a real database (Postgres, SQLite, etc.) when you're ready.
