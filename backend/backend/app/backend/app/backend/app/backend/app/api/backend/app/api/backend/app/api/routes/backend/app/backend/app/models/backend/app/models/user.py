
import uuid

from datetime import datetime

from sqlalchemy import (
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    func
)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False
    )

    preferred_language: Mapped[str] = mapped_column(
        String(10),
        default="te",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class WalletAccount(Base):

    __tablename__ = "wallet_accounts"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "account_type",
            name="uq_user_account_type"
        ),
        CheckConstraint(
            "balance >= 0",
            name="ck_wallet_non_negative"
        )
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    account_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    balance: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False
    )

    currency_code: Mapped[str] = mapped_column(
        String(20),
        default="VPOINT",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
  
