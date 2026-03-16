from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from src.Common.Enums.SubmissionStatus import SubmissionStatus


class SubmissionBase(BaseModel):
    name: str = Field(..., min_length=1)
    status: SubmissionStatus = SubmissionStatus.NEW


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    status: Optional[SubmissionStatus] = None


class BindResult(BaseModel):
    status: SubmissionStatus
    attempts: int


class SubmissionRead(BaseModel):
    id: int
    name: str
    status: SubmissionStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

