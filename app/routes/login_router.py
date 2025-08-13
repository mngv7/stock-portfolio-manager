from fastapi import APIRouter
import app.controllers.login_controller as lc

router = APIRouter()

router.post("/login")(lc.login)