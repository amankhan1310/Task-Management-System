from fastapi import APIRouter, HTTPException, status
from app.schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services import create_user, authenticate_user, get_user_by_username # Clean imports
from app.auth import create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    try:
        # Calling functions directly as defined in your user_service.py
        user = create_user(
            username=body.username,
            email=body.email,
            password=body.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    full_user = get_user_by_username(user["username"])
    return UserResponse(**dict(full_user))

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = authenticate_user(body.username, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=user["username"])

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

