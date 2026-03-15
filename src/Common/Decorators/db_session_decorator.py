from functools import wraps

from database import SessionLocal


def with_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            return func(session, *args, **kwargs)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper
