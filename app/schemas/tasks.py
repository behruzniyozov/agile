from pydantic import BaseModel


class TaskListProjectNested(BaseModel):
    key: str


class TaskListStatusNested(BaseModel):
    name: str


class TaskListUserNested(BaseModel):
    id: int
    email: str
    fullname: str | None


class TaskListResponse(BaseModel):
    id: int
    project: TaskListProjectNested
    key: str
    summary: str
    status: TaskListStatusNested
    priority: str


class TaskDetailResponse(BaseModel):
    id: int
    project: TaskListProjectNested
    key: str
    summary: str
    description: str | None
    status: TaskListStatusNested
    priority: str
    assignee: TaskListUserNested
    reporter: TaskListUserNested
    due_date: str


class TaskCreateRequest(BaseModel):
    project_id: int
    summary: str
    description: str | None
    status_id: int
    priority: str
    assignee_id: int
    reporter_id: int
    due_date: str


class TaskUpdateRequest(BaseModel):
    summary: str | None
    description: str | None
    status_id: int | None
    priority: str | None
    assignee_id: int | None
    reporter_id: int | None
    due_date: str | None


class TaskMoveRequest(BaseModel):
    status_id: int