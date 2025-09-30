from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enums import RoleEnum

from database import Base


class TimeStampMixin:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100))
    fullname: Mapped[str] = mapped_column(String(100), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(SQLAlchemyEnum(RoleEnum), nullable=False, default=RoleEnum.user)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    owned_projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="owner"
    )
    member_projects: Mapped[list["ProjectMember"]] = relationship(
        "ProjectMember", back_populates="user"
    )
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
    assigned_tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="assignee", foreign_keys="Task.assignee_id"
    )
    reported_tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="reporter", foreign_keys="Task.reporter_id"
    )
    received_notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="recipient",
        foreign_keys="Notification.recipient_id",
    )
    sent_notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="sender", foreign_keys="Notification.sender_id"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="user"
    )

    def __str__(self):
        return f"User(username={self.username}, email={self.email})"


class Project(Base, TimeStampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    key: Mapped[str] = mapped_column(String(10), nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)

    owner: Mapped["User"] = relationship("User", back_populates="owned_projects")
    members: Mapped[list["ProjectMember"]] = relationship(
        "ProjectMember", back_populates="project"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="project"
    )
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")

    def __str__(self):
        return f"Project(name={self.key})"


class ProjectMember(Base):
    __tablename__ = "project_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    joined_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    project: Mapped["Project"] = relationship("Project", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="member_projects")

    def __str__(self):
        return f"ProjectMember(user_id={self.user_id}, project_id={self.project_id})"


class Task(Base, TimeStampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    key: Mapped[str] = mapped_column(String(20), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status_id: Mapped[int] = mapped_column(
        ForeignKey("statuses.id", ondelete="CASCADE")
    )
    priority: Mapped[str] = mapped_column(String(10), nullable=False)
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    due_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    status: Mapped["Status"] = relationship("Status", back_populates="tasks")
    assignee: Mapped["User"] = relationship(
        "User", back_populates="assigned_tasks", foreign_keys="Task.assignee_id"
    )
    reporter: Mapped["User"] = relationship(
        "User", back_populates="reported_tasks", foreign_keys="Task.reporter_id"
    )
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="task")
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="task"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog", back_populates="task"
    )

    def __str__(self):
        return f"Task(summary={self.summary})"


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="status")

    def __str__(self):
        return f"Status(name={self.name})"


class Comment(Base, TimeStampMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(255), nullable=False)

    task: Mapped["Task"] = relationship("Task", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="comments")

    def __str__(self):
        return f"Comment(user_id={self.user_id})"


class Notification(Base, TimeStampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    recipient: Mapped["User"] = relationship(
        "User",
        back_populates="received_notifications",
        foreign_keys="Notification.recipient_id",
    )
    sender: Mapped["User"] = relationship(
        "User",
        back_populates="sent_notifications",
        foreign_keys="Notification.sender_id",
    )
    task: Mapped["Task"] = relationship("Task", back_populates="notifications")
    project: Mapped["Project"] = relationship("Project", back_populates="notifications")

    def __str__(self):
        return f"Notification(user_id={self.recipient_id})"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="audit_logs")
    task: Mapped["Task"] = relationship("Task", back_populates="audit_logs")

    def __str__(self):
        return f"AuditLog(user_id={self.user_id})"
