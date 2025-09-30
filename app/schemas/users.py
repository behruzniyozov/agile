from pydantic import BaseModel, EmailStr


class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    fullname: str
    avatar: str
    role: str
    is_active: bool

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "bY9vD@example.com",
                "fullname": "John Doe",
                "avatar": "https://example.com/avatar.jpg",
                "role": "developer",
                "is_active": True,
            }
        },
    }


class ProfileUpdateRequest(BaseModel):
    fullname: str
    avatar: str