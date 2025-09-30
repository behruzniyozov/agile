from fastapi import APIRouter, HTTPException, Response

from app.dependencies import current_user_dep, db_dep
from app.models import Comment
from app.schemas import CommentCreateRequest, CommentResponse, CommentUpdateRequest

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{comment_id}/", response_model=CommentResponse)
async def detail_comment(current_user: current_user_dep, db: db_dep, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.post("/comments/create/", response_model=CommentResponse)
async def write_comment(
    current_user: current_user_dep, db: db_dep, data: CommentCreateRequest
):
    comment = Comment(
        task_id=data.task_id,
        user_id=current_user.id,
        content=data.content,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@router.put("/comments/{comment_id}/update/", response_model=CommentResponse)
async def update_comment(
    current_user: current_user_dep,
    db: db_dep,
    comment_id: int,
    data: CommentUpdateRequest,
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only update your own comments"
        )

    for attr, value in data:
        setattr(comment, attr, value)

    db.commit()
    db.refresh(comment)

    return comment


@router.delete("/comments/{comment_id}/delete/")
async def delete_comment(current_user: current_user_dep, db: db_dep, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only delete your own comments"
        )

    db.delete(comment)
    db.commit()

    return Response(status_code=204)