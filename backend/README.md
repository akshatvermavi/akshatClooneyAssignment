# Backend (Clooney Asana Clone)

FastAPI-based backend that approximates Asana's Home/Projects/Tasks APIs for the Clooney web app cloning agent assignment.

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

Run tests:

```bash
pytest
```

Environment variables are configured via the root `.env` (see `.env.template`).
