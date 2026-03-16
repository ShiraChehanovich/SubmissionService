import os

from dotenv import load_dotenv

load_dotenv()

BIND_SERVICE_URL = os.getenv("BIND_SERVICE_BASE_URL")
MAX_BIND_ATTEMPTS = int(os.getenv("MAX_BIND_ATTEMPTS", "5"))
INITIAL_BACKOFF_SECONDS = float(os.getenv("INITIAL_BACKOFF_SECONDS", "0.5"))
