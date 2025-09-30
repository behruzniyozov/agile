import os
import shutil
from typing import Any, ClassVar
from uuid import uuid4

from fastapi import UploadFile
from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import EnumField, ImageField, PasswordField

from enums import RoleEnum, StatusEnum
from settings import MEDIA_PATH
from utils import hash_password


class UserAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "email",
        PasswordField("password"),
        "fullname",
        ImageField("avatar"),
        EnumField("role", enum=RoleEnum),
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = [
        "password",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at", "updated_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "email",
        "username",
        "is_active",
        "created_at",
        "updated_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]

    async def create(self, request: Request, data: dict[str, Any]):
        if "password" in data:
            data["password"] = hash_password(data["password"])

        print("Create is working!")
        print("=======================", "avatar" in data, data["avatar"])

        # if "avatar" in data:
        #     # Handle the avatar upload
        #     avatar_file = data["avatar"]
        #     if isinstance(avatar_file, tuple) and len(avatar_file) > 0:
        #         avatar_file = avatar_file[0]  # Get the first file if it's a list

        #     print("--------------------------", avatar_file)

        #     if avatar_file and avatar_file.filename:
        #         avatar_filename = await self._handle_avatar_upload(avatar_file)
        #         print("================= Avatar filename", avatar_filename)
        #         data["avatar"] = avatar_filename  # Store only filename, not full path

        return await super().create(request, data)

    async def _handle_avatar_upload(self, file: UploadFile) -> str | None:
        """Handle avatar file upload and return filename"""
        file_name_original = os.path.splitext(file.filename)[0]
        file_ext = os.path.splitext(file.filename)[1]

        filename = f"{file_name_original}-{str(uuid4())[0:8]}{file_ext}"
        file_path = MEDIA_PATH / filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return filename


class ProjectAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "key",
        "name",
        "description",
        "owner",
        "is_active",
        "is_private",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = [
        "description",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at", "updated_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "key",
        "name",
        "description",
        "owner",
        "is_active",
        "is_private",
        "created_at",
        "updated_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class ProjectMemberAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "user",
        "project",
        "joined_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = ["joined_at"]
    exclude_fields_from_create: ClassVar[list[str]] = ["joined_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["joined_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "user_id",
        "project_id",
        "joined_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class TaskAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "key",
        "summary",
        "description",
        "project",
        EnumField("status", enum=StatusEnum),
        "priority",
        "assignee",
        "reporter",
        "due_date",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = [
        "description",
        "assignee",
        "reporter",
        "due_date",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at", "updated_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "key",
        "summary",
        "description",
        "project",
        "status",
        "priority",
        "assignee",
        "reporter",
        "due_date",
        "created_at",
        "updated_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class StatusAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "name",
        "description",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = []
    exclude_fields_from_create: ClassVar[list[str]] = []
    exclude_fields_from_edit: ClassVar[list[str]] = []
    export_fields: ClassVar[list[str]] = [
        "id",
        "name",
        "description",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class CommentAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "task",
        "user",
        "content",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at", "updated_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "task",
        "user",
        "content",
        "created_at",
        "updated_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class NotificationAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "recipient",
        "sender",
        "task",
        "project",
        "message",
        "is_read",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at", "updated_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "recipient_id",
        "sender_id",
        "task_id",
        "project_id",
        "message",
        "is_read",
        "created_at",
        "updated_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class AuditLogAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "user",
        "task",
        "action",
        "timestamp",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = ["task_id", "timestamp"]
    exclude_fields_from_create: ClassVar[list[str]] = ["timestamp"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["timestamp"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "user_id",
        "task_id",
        "action",
        "created_at",
        "updated_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]