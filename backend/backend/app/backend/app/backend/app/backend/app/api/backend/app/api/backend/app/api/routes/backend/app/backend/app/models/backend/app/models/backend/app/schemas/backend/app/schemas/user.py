
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$"
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserResponse(BaseModel):

    id: UUID
    username: str
    status: str
    preferred_language: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
  
