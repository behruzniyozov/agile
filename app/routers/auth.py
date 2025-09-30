from fastapi import APIRouter, HTTPException

from dependencies import db_dep, oauth2_form_dep
from enums import RoleEnum
from models import User
from schemas import TokenResponse, UserRegisterRequest
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from utils import create_jwt_token, hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)



@router.post("/register/")
async def register_user(
   db: db_dep, register_data: UserRegisterRequest
):
    # Check for existing email
    if db.query(User).filter(User.email == register_data.email).first():
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Check for existing username
    if db.query(User).filter(User.username == register_data.username).first():
        raise HTTPException(status_code=400, detail="Username is already taken")

    # Determine role
    is_first_user = db.query(User).count() == 0
    role = RoleEnum.admin if is_first_user else RoleEnum.user

    # Create user
    user = User(
        username=register_data.username,
        email=register_data.email,
        password=hash_password(register_data.password),
        role=role,
        is_deleted=False,
        is_active=True,  # or False if requiring email confirmation
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully", "user_id": user.id}

    # send confirmation email
    # token = generate_confirmation_token(email=user.email)

    # send_email.delay(
    #     to_email=user.email,
    #     subject="Confirm your registration to Bookla",
    #     body=f"You can click the link to confirm your email: {FRONTEND_URL}/auth/confirm/{token}/",
    # )

    # return {
    #     "detail": f"Confirmation email sent to {user.email}. Please confirm to finalize your registration.",
    # }

    return {"detail": "Registration successful."}


@router.post("/login/")
async def login(form_data: oauth2_form_dep, db: db_dep):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_jwt_token(
        {"email": user.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_jwt_token(
        {"email": user.email}, expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES
    )

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
    )