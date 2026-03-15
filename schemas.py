from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SubmissionStatusEnum(str, Enum):
    new = "new"
    bound = "bound"
    bind_failed = "bind_failed"


class SubmissionBase(BaseModel):
    name: str = Field(..., min_length=1)
    status: SubmissionStatusEnum = SubmissionStatusEnum.new


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    status: Optional[SubmissionStatusEnum] = None


class BindResult(BaseModel):
    status: SubmissionStatusEnum
    attempts: int


class SubmissionRead(BaseModel):
    id: int
    name: str
    status: SubmissionStatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

