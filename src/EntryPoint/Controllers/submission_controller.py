from typing import List

from fastapi import APIRouter, status

import schemas
from src.BL.SubmissionBL import (
    bind_submission as bl_bind,
    create_submission as bl_create,
    delete_submission as bl_delete,
    get_submission as bl_get,
    list_submissions as bl_list,
    update_submission as bl_update,
)
from src.EntryPoint.Controllers.submission_route_params import (
    NameQuery,
    StatusFilterQuery,
    SubmissionIdPath,
)

router = APIRouter()


@router.get("/submissions", response_model=List[schemas.SubmissionRead])
def list_submissions(
    status_filter: StatusFilterQuery = None,
    name: NameQuery = None,
):
    return bl_list(status_filter=status_filter, name=name)


@router.post(
    "/submissions",
    response_model=schemas.SubmissionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_submission(
    submission_in: schemas.SubmissionCreate
):
    return bl_create(submission_in)


@router.get("/submissions/{submission_id}", response_model=schemas.SubmissionRead)
def get_submission(submission_id: SubmissionIdPath):
    submission = bl_get(submission_id)
    return submission


@router.patch("/submissions/{submission_id}", response_model=schemas.SubmissionRead)
def update_submission(
    submission_id: SubmissionIdPath,
    submission_in: schemas.SubmissionUpdate,
):
    return bl_update(submission_id, submission_in)


@router.delete(
    "/submissions/{submission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_submission(submission_id: SubmissionIdPath):
    bl_delete(submission_id)
    return None


@router.post(
    "/submissions/{submission_id}/bind",
    response_model=schemas.BindResult,
)
def bind_submission(submission_id: SubmissionIdPath):
    return bl_bind(submission_id)

