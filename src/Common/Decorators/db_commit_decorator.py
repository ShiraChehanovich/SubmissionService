from functools import wraps

from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect


def db_commit(func):
    def _refresh_if_mapped(session, value):
        if value is None:
            return

        values = value if isinstance(value, (list, tuple, set)) else (value,)
        for item in values:
            try:
                state = inspect(item)
            except NoInspectionAvailable:
                continue

            if getattr(state, "mapper", None) is not None:
                session.refresh(item)

    @wraps(func)
    def wrapper(session, *args, **kwargs):
        response = func(session, *args, **kwargs)
        session.commit()
        _refresh_if_mapped(session, response)
        return response

    return wrapper
