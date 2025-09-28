from fastapi import APIRouter

router = APIRouter()

@router.get("/api/config")
def get_config():
    pass