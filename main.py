from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.Domain.Init.db_init import init_db
from src.EntryPoint.ExceptionFilters import register_exception_filters
from src.EntryPoint.Controllers.submission_controller import router as submission_router
from src.Common.Utils.config import FRONTEND_ORIGINS

app = FastAPI(title="Submission API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=FRONTEND_ORIGINS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

register_exception_filters(app)

init_db()
app.include_router(submission_router)
