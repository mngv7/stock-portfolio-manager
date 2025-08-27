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

@router.get("/ticker/price")
def get_ticker_history_day(ticker: str, timestamp: float):
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)

    try:
        start_dt = datetime.fromtimestamp(timestamp)

        end_dt = datetime.now()

        data = stock.history(
            start=start_dt.strftime("%Y-%m-%d"),
            end=end_dt.strftime("%Y-%m-%d"),
            interval="1d"
        )

        if data.empty:
            raise HTTPException(status_code=404, detail="No historical data found")
        
        prices = data["Close"].tolist()

        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
