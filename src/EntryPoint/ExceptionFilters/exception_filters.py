from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.Common.Exceptions.NotFoundException import NotFoundException


def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=exc.error_code, content={"detail": exc.message})


def register_exception_filters(app: FastAPI):
    app.add_exception_handler(NotFoundException, not_found_exception_handler)

