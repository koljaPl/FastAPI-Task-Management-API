from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_items():
    """Получить список items (TODO)"""
    return {"message": "Items endpoint - coming soon"}