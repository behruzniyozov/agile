from pydantic import BaseModel


class CommentUserNested(BaseModel):
    id: int
    email: str
    fullname: str | None


class CommentTaskNested(BaseModel):
    key: str


class CommentResponse(BaseModel):
    id: int
    user: CommentUserNested
    task: CommentTaskNested
    content: str


class CommentCreateRequest(BaseModel):
    task_id: int
    content: str


class CommentUpdateRequest(BaseModel):
    content: str