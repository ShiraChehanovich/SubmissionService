from fastapi import FastAPI
from src.Domain.Init.db_init import init_db
from src.EntryPoint.ExceptionFilters import register_exception_filters
from src.EntryPoint.Controllers.submission_controller import router as submission_router

app = FastAPI(title="Submission API")
register_exception_filters(app)

init_db()
app.include_router(submission_router)
