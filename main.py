from typing import List, Optional

import time

import httpx
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Submission API")

BIND_SERVICE_URL = "http://localhost:8001/bind"
MAX_BIND_ATTEMPTS = 5
INITIAL_BACKOFF_SECONDS = 0.5


@app.get("/submissions", response_model=List[schemas.SubmissionRead])
def list_submissions(
    status_filter: Optional[schemas.SubmissionStatusEnum] = Query(
        None, alias="status", description="Filter by status"
    ),
    name: Optional[str] = Query(
        None, alias="name", description="Search by partial name match"
    ),
    db: Session = Depends(get_db),
):
    stmt = select(models.Submission)

    if status_filter is not None:
        stmt = stmt.where(models.Submission.status == status_filter.value)

    if name is not None:
        like_pattern = f"%{name}%"
        stmt = stmt.where(models.Submission.name.ilike(like_pattern))

    submissions = db.execute(stmt).scalars().all()
    return submissions


@app.post(
    "/submissions",
    response_model=schemas.SubmissionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_submission(
    submission_in: schemas.SubmissionCreate, db: Session = Depends(get_db)
):
    submission = models.Submission(
        name=submission_in.name,
        status=submission_in.status.value,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@app.get("/submissions/{submission_id}", response_model=schemas.SubmissionRead)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.get(models.Submission, submission_id)
    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )
    return submission


@app.patch("/submissions/{submission_id}", response_model=schemas.SubmissionRead)
def update_submission(
    submission_id: int,
    submission_in: schemas.SubmissionUpdate,
    db: Session = Depends(get_db),
):
    submission = db.get(models.Submission, submission_id)
    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    data = submission_in.dict(exclude_unset=True)
    if "name" in data:
        submission.name = data["name"]
    if "status" in data:
        submission.status = data["status"].value

    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@app.delete(
    "/submissions/{submission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.get(models.Submission, submission_id)
    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    db.delete(submission)
    db.commit()
    return None


@app.post(
    "/submissions/{submission_id}/bind",
    response_model=schemas.BindResult,
)
def bind_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.get(models.Submission, submission_id)
    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    # Idempotent behavior: if already bound, do nothing and return current state.
    if submission.status == schemas.SubmissionStatusEnum.bound.value:
        return schemas.BindResult(
            status=schemas.SubmissionStatusEnum.bound,
            attempts=0,
        )

    attempts = 0
    backoff = INITIAL_BACKOFF_SECONDS

    while attempts < MAX_BIND_ATTEMPTS:
        attempts += 1
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.post(BIND_SERVICE_URL, json={"submission_id": submission_id})
        except httpx.RequestError:
            # Timeout or network-level error: retry with backoff
            if attempts >= MAX_BIND_ATTEMPTS:
                break
            time.sleep(backoff)
            backoff *= 2
            continue

        # Retry on 5xx responses
        if 500 <= response.status_code < 600:
            if attempts >= MAX_BIND_ATTEMPTS:
                break
            time.sleep(backoff)
            backoff *= 2
            continue

        # Non-5xx response; treat non-2xx as failure without further retries.
        if not (200 <= response.status_code < 300):
            break

        # Success path
        submission.status = schemas.SubmissionStatusEnum.bound.value
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return schemas.BindResult(
            status=schemas.SubmissionStatusEnum.bound,
            attempts=attempts,
        )

    # Final failure
    submission.status = schemas.SubmissionStatusEnum.bind_failed.value
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return schemas.BindResult(
        status=schemas.SubmissionStatusEnum.bind_failed,
        attempts=attempts,
    )

