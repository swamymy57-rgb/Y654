from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.user import User, WalletAccount
from app.models.wallet_transaction import WalletTransaction
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    new_user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        status="active",
        preferred_language="te"
    )

    try:
        async with db.begin():
            db.add(new_user)
            await db.flush()

            main_wallet = WalletAccount(
                user_id=new_user.id,
                account_type="MAIN",
                balance=100,
                currency_code="VPOINT"
            )

            bonus_wallet = WalletAccount(
                user_id=new_user.id,
                account_type="BONUS",
                balance=0,
                currency_code="VPOINT"
            )

            db.add_all([main_wallet, bonus_wallet])
            await db.flush()

            welcome_transaction = WalletTransaction(
                wallet_account_id=main_wallet.id,
                transaction_type="CREDIT",
                amount=100,
                balance_after=100,
                description="Welcome virtual points"
            )

            db.add(welcome_transaction)

        return new_user

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
