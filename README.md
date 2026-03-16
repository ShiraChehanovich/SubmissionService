## Submission API (FastAPI + SQLite)

This project implements a simple CRUD API for managing `Submission` records using FastAPI and SQLite.

### Data model

Each submission has:
- **id**: integer primary key
- **name**: required string
- **status**: one of `new | bound | bind_failed`
- **created_at**: timestamp
- **updated_at**: timestamp

### Running with Docker Compose

This is the easiest way to run the full stack (submission service + bind service + frontend client) together.

**Prerequisites:** Make sure [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed.

1. From the project root (the `Submission` folder), run:

```bash
docker compose up
```

> Add `-d` to run in detached (background) mode:
> ```bash
> docker compose up -d
> ```

2. The following services will start:

| Service            | Container          | Port                          |
|--------------------|--------------------|-------------------------------|
| Submission API     | `submission`       | `http://localhost:8000`       |
| Bind Service       | `bind-service`     | `http://localhost:8001`       |
| Frontend Client    | `submission-client`| `http://localhost:3000`       |

3. To stop all services:

```bash
docker compose down
```

---

### Running with Docker (single service only)

Build the image:

```bash
docker build -t submission-api .
```

Run the container and expose API port `8000`:

```bash
docker run --rm -p 8000:8000 --name submission-api submission-api
```

### Environment configuration

Configuration is loaded from `.env` (see `.env.example`).

```bash
BIND_SERVICE_BASE_URL=http://localhost:8001
MAX_BIND_ATTEMPTS=5
INITIAL_BACKOFF_SECONDS=0.5
FRONTEND_ORIGINS=http://localhost:3000,http://127.0.0.1:5173
```

Then open the interactive API docs at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Endpoints

- **GET** `/submissions`  
  Optional query params:
  - `status` – filter by status
  - `name` – partial match search on `name`

- **POST** `/submissions`
- **GET** `/submissions/{id}`
- **PATCH** `/submissions/{id}`
- **DELETE** `/submissions/{id}`

Validation errors automatically return HTTP 400; missing records return HTTP 404.

