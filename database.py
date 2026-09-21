from typing import Dict, List, Optional
from threading import Lock

from models import Account, AccountCreate


class AccountDatabase:
    def __init__(self) -> None:
        self._accounts: Dict[int, Account] = {}
        self._next_id: int = 1
        self._lock = Lock()
        self._seed()

    def _seed(self) -> None:
        seed_data = [
            AccountCreate(
                name="Alice Johnson",
                email="alice@example.com",
                phone="+1-555-0101",
                account_type="savings",
            ),
            AccountCreate(
                name="Bob Smith",
                email="bob@example.com",
                phone="+1-555-0102",
                account_type="checking",
            ),
            AccountCreate(
                name="Acme Corp",
                email="finance@acme.com",
                phone="+1-555-0103",
                account_type="business",
            ),
        ]
        for item in seed_data:
            self.create(item)

    def create(self, data: AccountCreate) -> Account:
        with self._lock:
            account = Account(
                id=self._next_id,
                balance=0.0,
                is_active=True,
                **data.model_dump(),
            )
            self._accounts[account.id] = account
            self._next_id += 1
            return account

    def get(self, account_id: int) -> Optional[Account]:
        return self._accounts.get(account_id)

    def list_all(self, account_type: Optional[str] = None) -> List[Account]:
        accounts = list(self._accounts.values())
        if account_type:
            accounts = [a for a in accounts if a.account_type == account_type]
        return accounts


db = AccountDatabase()
