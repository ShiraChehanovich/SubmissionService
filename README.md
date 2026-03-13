## Submission API (FastAPI + SQLite)

This project implements a simple CRUD API for managing `Submission` records using FastAPI and SQLite.

### Data model

Each submission has:
- **id**: integer primary key
- **name**: required string
- **status**: one of `new | bound | bind_failed`
- **created_at**: timestamp
- **updated_at**: timestamp

### Requirements

Install dependencies (preferably in a virtual environment):

```bash
pip install -r requirements.txt
```

### Running the server

From this folder:

```bash
uvicorn main:app --reload
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

