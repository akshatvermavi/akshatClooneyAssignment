from datetime import date, datetime

from pydantic import BaseModel, Field


class WorkspaceBase(BaseModel):
    name: str


class WorkspaceRead(WorkspaceBase):
    id: int

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    color: str | None = None
    icon: str | None = None


class ProjectCreate(ProjectBase):
    workspace_id: int


class ProjectRead(ProjectBase):
    id: int
    workspace_id: int

    class Config:
        from_attributes = True


class SectionBase(BaseModel):
    name: str
    order_index: int = 0


class SectionRead(SectionBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    name: str
    description: str | None = None
    status: str = Field(default="inbox")
    assignee: str | None = None
    due_date: date | None = None
    priority: str | None = None


class TaskCreate(TaskBase):
    project_id: int
    section_id: int | None = None


class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    assignee: str | None = None
    due_date: date | None = None
    priority: str | None = None
    section_id: int | None = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    section_id: int | None = None
    created_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True


class HomeProjectSummary(BaseModel):
    id: int
    name: str
    color: str | None
    icon: str | None


class HomeTaskSummary(BaseModel):
    id: int
    name: str
    project_id: int
    project_name: str
    status: str


class HomeResponse(BaseModel):
    my_tasks: list[HomeTaskSummary]
    recent_projects: list[HomeProjectSummary]
