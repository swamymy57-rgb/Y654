from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import WalletAccount
from app.models.wallet_transaction import WalletTransaction


async def get_main_wallet(
    db: AsyncSession,
    user_id: UUID
):
    result = await db.execute(
        select(WalletAccount).where(
            WalletAccount.user_id == user_id,
            WalletAccount.account_type == "MAIN"
        )
    )
    return result.scalar_one_or_none()


async def spend_points(
    db: AsyncSession,
    user_id: UUID,
    amount: int,
    description: str
):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    result = await db.execute(
        select(WalletAccount)
        .where(
            WalletAccount.user_id == user_id,
            WalletAccount.account_type == "MAIN"
        )
        .with_for_update()
    )

    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise LookupError("Wallet not found")

    if wallet.balance < amount:
        raise ValueError("Insufficient virtual points")

    wallet.balance -= amount

    transaction = WalletTransaction(
        wallet_account_id=wallet.id,
        transaction_type="DEBIT",
        amount=amount,
        balance_after=wallet.balance,
        description=description
    )

    db.add(transaction)
    await db.flush()

    return wallet


async def award_points(
    db: AsyncSession,
    user_id: UUID,
    amount: int,
    description: str
):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    result = await db.execute(
        select(WalletAccount)
        .where(
            WalletAccount.user_id == user_id,
            WalletAccount.account_type == "MAIN"
        )
        .with_for_update()
    )

    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise LookupError("Wallet not found")

    wallet.balance += amount

    transaction = WalletTransaction(
        wallet_account_id=wallet.id,
        transaction_type="CREDIT",
        amount=amount,
        balance_after=wallet.balance,
        description=description
    )

    db.add(transaction)
    await db.flush()

    return wallet
