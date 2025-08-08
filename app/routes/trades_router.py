from fastapi import APIRouter
import app.controllers.trades_controller as tc

router = APIRouter()

router.post("/users/{user_id}/trades")(tc.create_trade)
router.get("/users/{user_id}/trades")(tc.get_all_trades)
router.get("/users/{user_id}/trades/{trade_id}")(tc.get_trade_by_id)
router.delete("/users/{user_id}/trades/{trade_id}")(tc.delete_trade_by_id)
router.patch("/users/{user_id}/trades/{trade_id}")(tc.edit_trade_by_id)