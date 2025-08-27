from fastapi import APIRouter, Depends, HTTPException
import app.controllers.portfolio_controller as pc
from app.utils.auth import authenticate_token
from app.utils.auth import AuthUser
from pydantic import BaseModel
import yfinance as yf
from datetime import datetime

class TradeRequest(BaseModel):
    ticker: str
    avg_price: float
    quantity: int
    fee: float

class TickerHistoryRequest(BaseModel):
    ticker: str
    timestamp: float

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

@router.get("/portfolio/value")
def get_portfolio_historical_value(user: AuthUser = Depends(authenticate_token)):
    return pc.get_portfolio_historical_value(user.username)
