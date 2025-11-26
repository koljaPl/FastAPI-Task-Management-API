from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.schemas.auth import Token
from app.schemas.user import User, UserCreate
from app.services.user import UserService
from app.core.security import create_access_token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 совместимый эндпоинт для получения токена.
    Username и password передаются через form-data.
    """
    user = UserService.authenticate(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = create_access_token(data={"sub": str(user.id)})

    return Token(access_token=access_token)


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""

    # Проверка существования email
    if UserService.get_by_email(db, user_in.email):
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # Проверка существования username
    if UserService.get_by_username(db, user_in.username):
        raise HTTPException(
            status_code=400,
            detail="User with this username already exists"
        )

    user = UserService.create(db, user_in)
    return user


@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Получить информацию о текущем пользователе"""
    return current_user