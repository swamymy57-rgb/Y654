from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User, WalletAccount
from app.models.wallet_transaction import WalletTransaction
from app.schemas.wallet import (
    WalletResponse,
    WalletTransactionResponse
)


router = APIRouter(prefix="/wallet", tags=["Virtual Wallet"])


@router.get("/me", response_model=WalletResponse)
async def my_wallet(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WalletAccount).where(
            WalletAccount.user_id == user.id,
            WalletAccount.account_type == "MAIN"
        )
    )

    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Virtual wallet not found"
        )

    return wallet


@router.get(
    "/transactions",
    response_model=list[WalletTransactionResponse]
)
async def my_transactions(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WalletTransaction)
        .join(
            WalletAccount,
            WalletTransaction.wallet_account_id == WalletAccount.id
        )
        .where(
            WalletAccount.user_id == user.id,
            WalletAccount.account_type == "MAIN"
        )
        .order_by(WalletTransaction.created_at.desc())
        .limit(50)
    )

    return result.scalars().all()
