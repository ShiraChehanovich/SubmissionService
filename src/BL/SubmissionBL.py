from typing import List, Optional

import time

import httpx

import schemas
from src.Common.Exceptions.NotFoundException import NotFoundException
from src.Common.Utils.config import BIND_SERVICE_URL, INITIAL_BACKOFF_SECONDS, MAX_BIND_ATTEMPTS
from src.Models import submission_model
from src.Models.submission_model import Submission


def _get_submission_or_raise(submission_id: int) -> Submission:
    submission = submission_model.get_submission(submission_id)
    if submission is None:
        raise NotFoundException()
    return submission


def _post_bind_request(submission_id: int) -> httpx.Response:
    with httpx.Client(timeout=5.0) as client:
        return client.post(f"{BIND_SERVICE_URL}/bind", json={"submission_id": submission_id})


def _is_retryable_response(response: httpx.Response) -> bool:
    return 500 <= response.status_code < 600


def _run_bind_attempt(submission_id: int) -> tuple[bool, bool]:
    """Returns (is_success, should_retry)."""
    try:
        response = _post_bind_request(submission_id)
    except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.WriteTimeout):
        return False, True
    except httpx.RequestError:
        return False, False

    if 200 <= response.status_code < 300:
        return True, False
    if _is_retryable_response(response):
        return False, True
    return False, False


def _apply_bind_status(
    submission_id: int,
    status: schemas.SubmissionStatus,
    attempts: int,
) -> schemas.BindResult:
    submission = submission_model.set_submission_status(submission_id, status.value)
    if submission is None:
        raise NotFoundException()
    return schemas.BindResult(status=status, attempts=attempts)


def list_submissions(
    status_filter: Optional[schemas.SubmissionStatus] = None,
    name: Optional[str] = None,
) -> List[Submission]:
    status_value = status_filter.value if status_filter is not None else None
    return submission_model.list_submissions(status_filter=status_value, name=name)

def create_submission(submission_in: schemas.SubmissionCreate) -> Submission:
    return submission_model.create_submission(
        name=submission_in.name,
        status=submission_in.status.value,
    )


def get_submission(submission_id: int) -> Submission:
    return submission_model.get_submission(submission_id)


def update_submission(
    submission_id: int,
    submission_in: schemas.SubmissionUpdate,
) -> Submission:
    data = submission_in.model_dump(exclude_unset=True)
    status_value = data["status"].value if "status" in data else None
    return submission_model.update_submission(
        submission_id,
        name=data.get("name"),
        status=status_value,
    )


def delete_submission(submission_id: int) -> None:
    return submission_model.delete_submission(submission_id)


def bind_submission(submission_id: int) -> schemas.BindResult:
    submission = _get_submission_or_raise(submission_id)

    if submission.status == schemas.SubmissionStatus.BOUND.value:
        return schemas.BindResult(status=schemas.SubmissionStatus.BOUND, attempts=0)

    attempts = 0
    backoff = INITIAL_BACKOFF_SECONDS

    while attempts < MAX_BIND_ATTEMPTS:
        attempts += 1
        is_success, should_retry = _run_bind_attempt(submission_id)
        if is_success:
            return _apply_bind_status(
                submission_id,
                schemas.SubmissionStatus.BOUND,
                attempts,
            )

        if not should_retry or attempts >= MAX_BIND_ATTEMPTS:
            break

        time.sleep(backoff)
        backoff *= 2

    return _apply_bind_status(
        submission_id,
        schemas.SubmissionStatus.BIND_FAILED,
        attempts,
    )
