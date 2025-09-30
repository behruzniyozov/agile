from fastapi import APIRouter, HTTPException, Response

from dependencies import (
    admin_user_dep,
    current_user_dep,
    db_dep,
    task_creatable_user_dep,
)
from models import Project, Status, Task
from schemas import (
    TaskCreateRequest,
    TaskDetailResponse,
    TaskListResponse,
    TaskMoveRequest,
    TaskUpdateRequest,
)
from services import generate_task_key

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/all/", response_model=list[TaskListResponse])
async def get_tasks(admin_user: admin_user_dep, db: db_dep):
    """Admin only"""
    tasks = db.query(Task).all()

    return tasks


@router.get("/{task_key}/")
async def get_task_by_key(current_user: current_user_dep, db: db_dep, task_key: str):
    task = db.query(Task).filter(Task.key == task_key).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/create/", response_model=TaskDetailResponse)
async def create_task(
    current_user: task_creatable_user_dep, db: db_dep, data: TaskCreateRequest
):
    project = db.query(Project).filter(Project.id == data.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    task = Task(
        project_id=data.project_id,
        summary=data.summary,
        description=data.description,
        key=generate_task_key(db=db, project=project),
        status_id=data.status_id,
        priority=data.priority,
        reporter_id=current_user.id,
        assignee_id=data.assignee_id,
        due_date=data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.put("/{task_id}/update/", response_model=TaskDetailResponse)
async def update_task(
    current_user: task_creatable_user_dep,
    db: db_dep,
    task_id: int,
    data: TaskUpdateRequest,
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.reporter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to update this task"
        )

    for attr, value in data:
        setattr(task, attr, value)

    db.commit()
    db.refresh(task)

    return task


@router.patch("/{task_id}/move/", response_model=TaskDetailResponse)
async def move_task(
    current_user: current_user_dep, db: db_dep, task_id: int, status_id: TaskMoveRequest
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    status = db.query(Status).filter(Status.id == status_id).first()

    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    task.status_id = status_id

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}/delete/")
async def delete_task(current_user: task_creatable_user_dep, db: db_dep, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.reporter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this task"
        )

    db.delete(task)
    db.commit()

    return Response(status_code=204)


@router.get("/{task_key}/comments/")
async def get_task_comments(current_user: current_user_dep, db: db_dep, task_key: str):
    task = db.query(Task).filter(Task.key == task_key).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comments = task.comments.all()

    return comments