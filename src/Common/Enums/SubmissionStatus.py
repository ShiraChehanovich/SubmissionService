from enum import Enum


class SubmissionStatus(str, Enum):
    NEW = "new"
    BOUND = "bound"
    BIND_FAILED = "bind_failed"
