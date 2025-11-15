from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from .deps import get_db_dep

router = APIRouter(prefix="/home", tags=["home"])


@router.get("", response_model=schemas.HomeResponse)
def get_home(db: Session = Depends(get_db_dep)):
    """Approximate Asana Home page summary.

    Returns:
    - recent_projects: last updated projects
    - my_tasks: tasks assigned to the synthetic user "me"
    """

    return crud.get_home_summary(db)
