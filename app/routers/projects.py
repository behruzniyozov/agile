from fastapi import APIRouter, HTTPException

from dependencies import (
    admin_user_dep,
    current_user_dep,
    db_dep,
    management_user_dep,
)
from models import Project, User
from schemas import (
    ProjectCreateRequest,
    ProjectInviteRequest,
    ProjectKickRequest,
    ProjectMemberResponse,
    ProjectResponse,
    ProjectUpdateRequest,
    TaskListResponse,
)
from services import generate_project_key

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/all/", response_model=list[ProjectResponse])
async def get_all_projects(admin_user: admin_user_dep, db: db_dep):
    """Admin only"""
    projects = db.query(Project).all()

    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")

    return projects


@router.get("/joined/")
async def get_joined_projects(current_user: current_user_dep, db: db_dep):
    """List of projects user has joined"""
    # joined_projects =
    pass


@router.get("/{project_key}/", response_model=ProjectResponse)
async def get_project_by_id(db: db_dep, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.post("/create/")
async def create_project(
    user: management_user_dep, db: db_dep, data: ProjectCreateRequest
):
    generated_key = generate_project_key(db=db, name=data.name)

    project = Project(
        name=data.name,
        key=generated_key,
        description=data.description,
        is_private=data.is_private,
        owner_id=user.id,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.put("/{project_key}/update/")
async def update_project(
    user: management_user_dep, db: db_dep, project_key: str, data: ProjectUpdateRequest
):
    project = db.query(Project).filter(Project.key == project_key).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for attr, value in data:
        setattr(project, attr, value)

    if "name" in data:
        project.key = generate_project_key(db=db, name=data.name)

    db.commit()
    db.refresh(project)

    return project


### Members


@router.get("/{project_key}/members/", response_model=list[ProjectMemberResponse])
async def get_project_members(user: current_user_dep, db: db_dep, project_key: str):
    project = db.query(Project).filter(Project.key == project_key).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = project.members.all()

    return members


@router.post("/{project_key}/members/invite/")
async def invite_project_member(
    user: management_user_dep,
    db: db_dep,
    project_key: str,
    invite_data: ProjectInviteRequest,
):
    project = db.query(Project).filter(Project.key == project_key).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    user = db.query(User).filter(User.id == invite_data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found to invite")

    if user in project.members:
        raise HTTPException(status_code=400, detail="User is already in the project")

    project.members.append(user)
    db.commit()
    db.refresh(project)

    return project


@router.post("/{project_key}/members/kick/")
async def kick_project_member(
    user: management_user_dep,
    db: db_dep,
    project_key: str,
    kick_data: ProjectKickRequest,
):
    project = db.query(Project).filter(Project.key == project_key).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    user = db.query(User).filter(User.id == kick_data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found to kick")

    if user not in project.members:
        raise HTTPException(status_code=400, detail="User is not in the project")

    project.members.remove(user)
    db.commit()
    db.refresh(project)

    return project


@router.get("/{project_key}/tasks/", response_model=list[TaskListResponse])
async def get_project_tasks(
    current_user: current_user_dep, db: db_dep, project_key: str
):
    project = db.query(Project).filter(Project.key == project_key).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = project.tasks.all()

    return tasks