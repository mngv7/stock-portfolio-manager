from fastapi import APIRouter
import app.controllers.portfolio_controller as pc

router = APIRouter()

router.get("/users/{user_id}/portfolio")(pc.get_portfolio_by_user_id)