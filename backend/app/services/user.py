from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """Получить пользователя по email"""
        return db.scalar(select(User).where(User.email == email))

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        """Получить пользователя по username"""
        return db.scalar(select(User).where(User.username == username))

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        """Получить пользователя по ID"""
        return db.get(User, user_id)

    @staticmethod
    def create(db: Session, user_in: UserCreate) -> User:
        """Создать пользователя"""
        user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> User | None:
        """Аутентификация пользователя"""
        user = UserService.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user