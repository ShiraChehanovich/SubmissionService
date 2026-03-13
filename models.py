from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String

from database import Base


class SubmissionStatus(str):
    NEW = "new"
    BOUND = "bound"
    BIND_FAILED = "bind_failed"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    status = Column(
        Enum(
            SubmissionStatus.NEW,
            SubmissionStatus.BOUND,
            SubmissionStatus.BIND_FAILED,
            name="submission_status",
        ),
        nullable=False,
        default=SubmissionStatus.NEW,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

