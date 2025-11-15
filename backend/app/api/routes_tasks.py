from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from .deps import get_db_dep, get_object_or_404

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db_dep)):
    # Validate that project exists (and section if provided)
    project = crud.get_project(db, task_in.project_id)
    get_object_or_404(project, detail="Project not found")

    if task_in.section_id is not None:
        section = db.get(models.Section, task_in.section_id)
        if section is None or section.project_id != task_in.project_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid section_id")

    task = crud.create_task(db, task_in)
    return schemas.TaskRead.model_validate(task)


@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db_dep)):
    task = crud.get_task(db, task_id)
    get_object_or_404(task, detail="Task not found")
    return schemas.TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db_dep)):
    task = crud.get_task(db, task_id)
    get_object_or_404(task, detail="Task not found")
    updated = crud.update_task(db, task, task_in)
    return schemas.TaskRead.model_validate(updated)
