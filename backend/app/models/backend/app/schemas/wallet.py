from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WalletResponse(BaseModel):
    account_type: str
    balance: int
    currency_code: str

    model_config = ConfigDict(from_attributes=True)


class WalletTransactionResponse(BaseModel):
    id: UUID
    transaction_type: str
    amount: int
    balance_after: int
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
