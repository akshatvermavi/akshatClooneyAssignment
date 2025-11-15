# Clooney - Web App Cloning Agent (Asana Home/Projects/Tasks)

This repository contains a **frontend** (React + Tailwind) and **backend** (FastAPI) implementation for a Clooney-style web app cloning agent that targets Asana's Home, Projects, and Tasks pages.

- `frontend/` – React app with Tailwind and Playwright-based visual & CSS tests
- `backend/` – FastAPI service with OpenAPI spec (`api.yml`), `schema.sql`, and exhaustive tests for key endpoints

## Quick start

1. Copy `.env.template` to `.env` and adjust values if needed.
2. Backend:
   ```bash
   cd backend
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
3. Frontend (in another terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Tests

- Backend: `cd backend && pytest`
- Frontend visual/CSS tests (requires `npm run dev` running):
  ```bash
  cd frontend
  npm run test:e2e
  ```

See `frontend/README.md` and `backend/README.md` for more details.
