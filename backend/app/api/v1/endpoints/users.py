from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    """Получить список пользователей (TODO)"""
    return {"message": "Users endpoint - coming soon"}