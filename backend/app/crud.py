from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


# Workspaces

def get_or_create_default_workspace(db: Session, name: str) -> models.Workspace:
    stmt = select(models.Workspace).where(models.Workspace.name == name)
    workspace = db.scalar(stmt)
    if workspace:
        return workspace
    workspace = models.Workspace(name=name)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


def list_workspaces(db: Session) -> Sequence[models.Workspace]:
    stmt = select(models.Workspace).order_by(models.Workspace.id)
    return list(db.scalars(stmt))


# Projects

def create_project(db: Session, project_in: schemas.ProjectCreate) -> models.Project:
    project = models.Project(**project_in.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session, workspace_id: int | None = None) -> Sequence[models.Project]:
    stmt = select(models.Project)
    if workspace_id is not None:
        stmt = stmt.where(models.Project.workspace_id == workspace_id)
    stmt = stmt.order_by(models.Project.updated_at.desc())
    return list(db.scalars(stmt))


def get_project(db: Session, project_id: int) -> models.Project | None:
    stmt = select(models.Project).where(models.Project.id == project_id)
    return db.scalar(stmt)


# Sections

def list_sections(db: Session, project_id: int) -> Sequence[models.Section]:
    stmt = (
        select(models.Section)
        .where(models.Section.project_id == project_id)
        .order_by(models.Section.order_index)
    )
    return list(db.scalars(stmt))


# Tasks

def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    task = models.Task(**task_in.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(
    db: Session,
    *,
    project_id: int | None = None,
    assignee: str | None = None,
    status: str | None = None,
) -> Sequence[models.Task]:
    stmt = select(models.Task)
    if project_id is not None:
        stmt = stmt.where(models.Task.project_id == project_id)
    if assignee is not None:
        stmt = stmt.where(models.Task.assignee == assignee)
    if status is not None:
        stmt = stmt.where(models.Task.status == status)
    stmt = stmt.order_by(models.Task.created_at.desc())
    return list(db.scalars(stmt))


def get_task(db: Session, task_id: int) -> models.Task | None:
    stmt = select(models.Task).where(models.Task.id == task_id)
    return db.scalar(stmt)


def update_task(db: Session, task: models.Task, task_in: schemas.TaskUpdate) -> models.Task:
    data = task_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# Home summaries

def get_home_summary(db: Session, me_assignee: str = "me") -> schemas.HomeResponse:
    # Recent projects
    projects = list_projects(db)
    recent_projects = [
        schemas.HomeProjectSummary(
            id=p.id,
            name=p.name,
            color=p.color,
            icon=p.icon,
        )
        for p in projects[:8]
    ]

    # My tasks (assigned to "me")
    tasks = list_tasks(db, assignee=me_assignee)
    project_by_id = {p.id: p for p in projects}
    my_tasks = []
    for t in tasks[:20]:
        project = project_by_id.get(t.project_id)
        my_tasks.append(
            schemas.HomeTaskSummary(
                id=t.id,
                name=t.name,
                project_id=t.project_id,
                project_name=project.name if project else "Unknown",
                status=t.status,
            )
        )

    return schemas.HomeResponse(my_tasks=my_tasks, recent_projects=recent_projects)
