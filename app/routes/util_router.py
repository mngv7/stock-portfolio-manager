from fastapi import APIRouter
from app.services.parameter_store.parameter_store import fetch_parameter_local
import os

router = APIRouter()

@router.get("/api/config")
def get_config():
    pass