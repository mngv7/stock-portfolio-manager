from fastapi import APIRouter
from app.utils.parameter_store import fetch_parameter_local
import os

router = APIRouter()

@router.get("/api/config")
def get_config():
    env = os.getenv("VITE_BUILD_ENV", "dev")
    parameter_name = f"/n11592931/{env}/backend/api_url"

    api_url = fetch_parameter_local(parameter_name)
    if api_url is None:
        return {"api_url": None, "error": "Parameter not found"}
    return {"api_url": api_url}