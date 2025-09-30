from pydantic import BaseModel

from enums import RoleEnum


class ProjectOwnerNested(BaseModel):
    id: int
    email: str
    fullname: str | None = None
    avatar: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    key: str
    description: str | None = None
    owner: ProjectOwnerNested

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Project 1",
                "key": "P1",
                "description": "Project description",
                "owner": {
                    "id": 1,
                    "email": "bY9vD@example.com",
                    "fullname": "John Doe",
                },
            }
        },
    }


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None
    is_private: bool | None = False


class ProjectUpdateRequest(BaseModel):
    name: str | None
    description: str | None
    is_private: bool | None


class ProjectInviteRequest(BaseModel):
    user_id: int
    role: RoleEnum


class ProjectKickRequest(BaseModel):
    user_id: int


class ProjectMemberResponse(BaseModel):
    id: int
    user: ProjectOwnerNested
    joined_at: str