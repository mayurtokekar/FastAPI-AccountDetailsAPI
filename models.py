from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    account_type: str = Field(..., pattern="^(savings|checking|business)$")


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    balance: float = 0.0
    is_active: bool = True


class AccountSummary(BaseModel):
    id: int
    name: str
    email: EmailStr
    account_type: str


class AccountList(BaseModel):
    total: int
    accounts: List[AccountSummary]
