from fastapi import APIRouter, Depends
import app.controllers.portfolio_controller as pc
from app.utils.auth import authenticate_token
from app.utils.auth import AuthUser
from pydantic import BaseModel

class TradeRequest(BaseModel):
    ticker: str
    avg_price: float
    quantity: int
    fee: float

router = APIRouter()

@router.get("/portfolio/assets")
def get_portfolio_assets(user: AuthUser = Depends(authenticate_token)):
    return pc.get_portfolio_assets(user.username)

@router.post("/portfolio/trades")
def log_trade(trade: TradeRequest, user: AuthUser = Depends(authenticate_token)):
    return pc.log_trade(user.username, trade.ticker, trade.avg_price, trade.quantity, trade.fee)

@router.get("/portfolio/trades")
def get_trade_history(user: AuthUser = Depends(authenticate_token)):
    return pc.get_trade_history(user.username)
