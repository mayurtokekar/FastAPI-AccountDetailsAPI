from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse

from database import db
from models import Account, AccountCreate, AccountList, AccountSummary

app = FastAPI(
    title="Account Details API",
    description="A simple FastAPI service to fetch and manage account details.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root() -> dict:
    return {"status": "ok", "service": "account-details-api"}


@app.get("/health", tags=["Health"])
def health() -> dict:
    return {"status": "healthy"}


@app.get(
    "/accounts",
    response_model=AccountList,
    tags=["Accounts"],
    summary="List all accounts",
)
def list_accounts(
    account_type: Optional[str] = Query(
        None,
        pattern="^(savings|checking|business)$",
        description="Filter by account type",
    ),
) -> AccountList:
    accounts = db.list_all(account_type=account_type)
    return AccountList(
        total=len(accounts),
        accounts=[
            AccountSummary(
                id=a.id,
                name=a.name,
                email=a.email,
                account_type=a.account_type,
            )
            for a in accounts
        ],
    )


@app.get(
    "/accounts/{account_id}",
    response_model=Account,
    tags=["Accounts"],
    summary="Fetch a single account by ID",
)
def get_account(account_id: int) -> Account:
    account = db.get(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with id {account_id} not found",
        )
    return account


@app.post(
    "/accounts",
    response_model=Account,
    status_code=status.HTTP_201_CREATED,
    tags=["Accounts"],
    summary="Create a new account",
)
def create_account(payload: AccountCreate) -> Account:
    return db.create(payload)


@app.exception_handler(HTTPException)
def http_exception_handler(_request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
