from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import SessionLocal
from enums import RoleEnum
from models import User
from settings import ALGORITHM, SECRET_KEY


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]

##### Authentication dependencies #####

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

oauth2_scheme_dep = Annotated[str, Depends(oauth2_scheme)]
oauth2_form_dep = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user(db: db_dep, token: oauth2_scheme_dep):
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True},
        )

        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        return user

    except JWTError as err:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from err
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=401, detail="Refresh token has expired"
        ) from err


current_user_dep = Annotated[User, Depends(get_current_user)]


async def get_admin_user(
    current_user: current_user_dep,
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=400, detail="User is not admin")
    return current_user


async def get_management_user(current_user: current_user_dep):
    if current_user.role not in [RoleEnum.admin, RoleEnum.manager]:
        raise HTTPException(
            status_code=400,
            detail="You are not admin or manager. You can't perform this action.",
        )
    return current_user


async def get_task_creatable_user(current_user: current_user_dep):
    if current_user.role not in [RoleEnum.admin, RoleEnum.manager, RoleEnum.tester]:
        raise HTTPException(
            status_code=400,
            detail="You are not admin, manager or tester. You can't perform this action.",
        )
    return current_user


admin_user_dep = Annotated[User, Depends(get_admin_user)]
management_user_dep = Annotated[User, Depends(get_management_user)]
task_creatable_user_dep = Annotated[User, Depends(get_task_creatable_user)]