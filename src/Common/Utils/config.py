import os

from dotenv import load_dotenv

load_dotenv()

BIND_SERVICE_URL = os.getenv("BIND_SERVICE_BASE_URL")
MAX_BIND_ATTEMPTS = int(os.getenv("MAX_BIND_ATTEMPTS", "5"))
INITIAL_BACKOFF_SECONDS = float(os.getenv("INITIAL_BACKOFF_SECONDS", "0.5"))

# Comma-separated list, e.g. "http://localhost:3000,http://127.0.0.1:5173"
FRONTEND_ORIGINS = [
	origin.strip()
	for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:3000").split(",")
	if origin.strip()
]

