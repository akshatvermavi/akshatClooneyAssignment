from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import Base, engine, SessionLocal
from .api import routes_home, routes_projects, routes_tasks
from . import crud, schemas


Base.metadata.create_all(bind=engine)

# Seed a default workspace and project so the UI has something to work with
with SessionLocal() as db:
    default_ws = crud.get_or_create_default_workspace(db, get_settings().asana_seed_workspace_name)
    existing_projects = crud.list_projects(db, workspace_id=default_ws.id)
    if not existing_projects:
        crud.create_project(
            db,
            schemas.ProjectCreate(
                name="My First Project",
                workspace_id=default_ws.id,
                color="#3a258e",
                icon="list",
            ),
        )

settings = get_settings()

app = FastAPI(
    title="Clooney Asana Clone API",
    version="0.1.0",
    description="Backend API approximating Asana Home/Projects/Tasks for the Clooney assignment.",
)

# CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes_home.router, prefix=settings.api_prefix)
app.include_router(routes_projects.router, prefix=settings.api_prefix)
app.include_router(routes_tasks.router, prefix=settings.api_prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}
