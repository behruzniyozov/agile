from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserRegisterRequest(BaseModel):
    email: str
    username: str
    password: str