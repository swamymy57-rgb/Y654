import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_transaction_amount_positive"),
        CheckConstraint(
            "transaction_type IN ('CREDIT', 'DEBIT')",
            name="ck_transaction_type_valid"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    wallet_account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("wallet_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    transaction_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    balance_after: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
