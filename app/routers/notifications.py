from fastapi import APIRouter, HTTPException

from app.dependencies import current_user_dep, db_dep
from app.models import Notification
from app.schemas import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/notifications/", response_model=list[NotificationResponse])
async def get_notifications(current_user: current_user_dep, db: db_dep):
    """User's notifications List"""
    notifications = current_user.received_notifications.all()

    return notifications


@router.put("/notifications/{notification_id}/", response_model=NotificationResponse)
async def read_notification(
    current_user: current_user_dep, db: db_dep, notification_id: int
):
    notification = (
        db.query(Notification).filter(Notification.id == notification_id).first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification