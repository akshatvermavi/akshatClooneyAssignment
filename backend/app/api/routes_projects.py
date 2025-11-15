from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from .deps import get_db_dep, get_object_or_404

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[schemas.ProjectRead])
def list_projects(
    workspace_id: int | None = Query(default=None, description="Filter by workspace id"),
    db: Session = Depends(get_db_dep),
):
    return [schemas.ProjectRead.model_validate(p) for p in crud.list_projects(db, workspace_id)]


@router.post("", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db_dep)):
    workspace = crud.list_workspaces(db)
    if not any(w.id == project_in.workspace_id for w in workspace):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid workspace_id")
    project = crud.create_project(db, project_in)
    return schemas.ProjectRead.model_validate(project)


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db_dep)):
    project = crud.get_project(db, project_id)
    get_object_or_404(project, detail="Project not found")
    return schemas.ProjectRead.model_validate(project)


@router.get("/{project_id}/sections", response_model=list[schemas.SectionRead])
def get_project_sections(project_id: int, db: Session = Depends(get_db_dep)):
    project = crud.get_project(db, project_id)
    get_object_or_404(project, detail="Project not found")
    sections: Sequence[models.Section] = crud.list_sections(db, project_id)
    return [schemas.SectionRead.model_validate(s) for s in sections]


@router.get("/{project_id}/tasks", response_model=list[schemas.TaskRead])
def get_project_tasks(
    project_id: int,
    status_filter: str | None = Query(
        default=None,
        alias="status",
        description="Optional status filter (e.g. inbox, today, completed)",
    ),
    assignee: str | None = Query(default=None, description="Assignee identifier"),
    db: Session = Depends(get_db_dep),
):
    project = crud.get_project(db, project_id)
    get_object_or_404(project, detail="Project not found")

    # Basic validation inspired by Asana semantics
    if status_filter is not None and len(status_filter) > 64:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="status too long",
        )

    tasks = crud.list_tasks(db, project_id=project_id, assignee=assignee, status=status_filter)
    return [schemas.TaskRead.model_validate(t) for t in tasks]
