from typing import Annotated, Optional

from fastapi import Path, Query

import schemas

StatusFilterQuery = Annotated[
    Optional[schemas.SubmissionStatus],
    Query(alias="status", description="Filter by status"),
]

NameQuery = Annotated[
    Optional[str],
    Query(alias="name", description="Search by partial name match"),
]

SubmissionIdPath = Annotated[
    int,
    Path(ge=1, description="Submission id"),
]

