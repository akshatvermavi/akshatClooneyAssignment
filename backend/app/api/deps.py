from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db


def get_db_dep(db: Session = Depends(get_db)) -> Session:
    return db


def get_object_or_404(obj, *, detail: str = "Object not found"):
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return obj
