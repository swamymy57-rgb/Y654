
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from app.database import get_db
from app.models.user import User, WalletAccount
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])

password_hasher = PasswordHash.recommended()


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
        password_hash=password_hasher.hash(
            payload.password
        ),
        status="active",
        preferred_language="te"
    )

    try:

        async with db.begin():

            db.add(new_user)

            await db.flush()

            db.add_all([
                WalletAccount(
                    user_id=new_user.id,
                    account_type="MAIN",
                    balance=1000
                ),
                WalletAccount(
                    user_id=new_user.id,
                    account_type="BONUS",
                    balance=0
                )
            ])

        return new_user

    except IntegrityError:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
      
