from fastapi import APIRouter
import app.controllers.portfolio_controller as pc
from pydantic import BaseModel

class TradeRequest(BaseModel):
    ticker: str
    avg_price: float
    quantity: int
    fee: float

router = APIRouter()

@router.get("/users/{username}/portfolio/assets")
def get_portfolio_assets(username: str):
    return pc.get_portfolio_assets(username)

@router.post("/users/{username}/portfolio/trades")
def log_trade(username: str, trade: TradeRequest):
    return pc.log_trade(username, trade.ticker, trade.avg_price, trade.quantity, trade.fee)

@router.get("/users/{username}/portfolio/trades")
def get_trade_history(username: str):
    return pc.get_trade_history(username)