from fastapi import APIRouter, HTTPException, UploadFile

from app.dependencies import current_user_dep, db_dep
from app.models import User
from app.schemas import ProfileResponse, ProfileUpdateRequest
from app.services import save_avatar_file, validate_image

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/users/{id}/", response_model=ProfileResponse)
async def get_user_by_id(db: db_dep, id: int):
    user = db.query(User).filter(User.id == id).first()

    if not user or (user.is_deleted):
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/profile/", response_model=ProfileResponse)
async def get_profile(current_user: current_user_dep):
    return current_user


@router.put("/profile/update/", response_model=ProfileResponse)
async def update_profile(
    db: db_dep, current_user: current_user_dep, data: ProfileUpdateRequest
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/avatar/upload/")
async def upload_avatar(cover: UploadFile):
    validated_image = validate_image(file=cover)

    file_url = save_avatar_file(file=validated_image)

    return {
        "url": file_url,
        "message": "Cover image uploaded successfully",
    }


@router.delete("/profile/delete/")
async def delete_profile(db: db_dep, current_user: current_user_dep):
    current_user.is_deleted = True
    current_user.is_active = False

    db.commit()

    return {
        "detail": "Profile deleted successfully",
    }