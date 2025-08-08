from fastapi import APIRouter
import app.controllers.users.users_controller as uc

router = APIRouter()

router.get("/users", response_model=list)(uc.get_all_users)
router.post("/users")(uc.create_user)
router.get("/users/{user_id}")(uc.get_user_by_id)
router.delete("/users/{user_id}")(uc.delete_user_by_id)