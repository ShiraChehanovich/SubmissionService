from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.Common.Decorators.db_commit_decorator import db_commit
from src.Common.Decorators.db_session_decorator import with_db_session
from src.Common.Entities.Submission import Submission
from src.Common.Exceptions.NotFoundException import NotFoundException


def _build_submission(name: str, status: str) -> Submission:
    return Submission(name=name, status=status)


def _list_submissions(
        db: Session,
        status_filter: Optional[str] = None,
        name: Optional[str] = None,
) -> List[Submission]:
    stmt = select(Submission)
    if status_filter is not None:
        stmt = stmt.where(Submission.status == status_filter)
    if name is not None:
        stmt = stmt.where(Submission.name.ilike(f"%{name}%"))
    return list(db.execute(stmt).scalars().all())


def _create_submission(db: Session, name: str, status: str) -> Submission:
    submission = _build_submission(name, status)
    db.add(submission)
    return submission


def _get_submission(db: Session, submission_id: int) -> Optional[Submission]:
    return db.get(Submission, submission_id)


def _update_submission(
        db: Session,
        submission_id: int,
        name: Optional[str] = None,
        status: Optional[str] = None,
) -> Submission:
    submission = _get_submission(db, submission_id)
    if submission is None:
        raise NotFoundException()
    if name is not None:
        submission.name = name
    if status is not None:
        submission.status = status
    return submission


def _delete_submission(db: Session, submission_id: int) -> None:
    submission = _get_submission(db, submission_id)
    if submission is None:
        raise NotFoundException()
    db.delete(submission)
    return None


def _set_submission_status(db: Session, submission_id: int, status: str) -> Optional[Submission]:
    submission = _get_submission(db, submission_id)
    if submission is None:
        return None
    submission.status = status
    return submission


@with_db_session
def list_submissions(
        db: Session,
        status_filter: Optional[str] = None,
        name: Optional[str] = None,
) -> List[Submission]:
    return _list_submissions(db, status_filter=status_filter, name=name)


@with_db_session
@db_commit
def create_submission(db: Session, name: str, status: str) -> Submission:
    return _create_submission(db, name=name, status=status)


@with_db_session
def get_submission(db: Session, submission_id: int) -> Optional[Submission]:
    submission = _get_submission(db, submission_id)
    if submission is None:
        raise NotFoundException()
    return submission


@with_db_session
@db_commit
def update_submission(
        db: Session,
        submission_id: int,
        name: Optional[str] = None,
        status: Optional[str] = None,
) -> Submission:
    return _update_submission(db, submission_id, name=name, status=status)


@with_db_session
@db_commit
def delete_submission(db: Session, submission_id: int) -> None:
    return _delete_submission(db, submission_id)


@with_db_session
@db_commit
def set_submission_status(
        db: Session,
        submission_id: int,
        status: str,
) -> Optional[Submission]:
    return _set_submission_status(db, submission_id, status)
