from pydantic import BaseModel


class NotificationUserNested(BaseModel):
    id: int
    email: str
    fullname: str | None


class NotificationTaskNested(BaseModel):
    key: str


class NotificationProjectNested(BaseModel):
    key: str


class NotificationResponse(BaseModel):
    id: int
    message: str
    recipient: NotificationUserNested
    sender: NotificationUserNested
    task: NotificationTaskNested | None
    project: NotificationProjectNested | None