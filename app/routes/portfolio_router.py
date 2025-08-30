from fastapi import APIRouter, Depends, Query
import app.controllers.portfolio_controller as pc
from app.utils.auth import authenticate_token
from app.utils.auth import AuthUser
from pydantic import BaseModel

class TradeRequest(BaseModel):
    ticker: str
    avg_price: float
    quantity: int
    fee: float
    timestamp: int

class TickerHistoryRequest(BaseModel):
    ticker: str
    timestamp: float

router = APIRouter()

@router.get("/api/v1/portfolio/assets")
def get_portfolio_assets(user: AuthUser = Depends(authenticate_token)):
    return pc.get_portfolio_assets(user.username)

@router.post("/api/v1/portfolio/trades")
def log_trade(trade: TradeRequest, user: AuthUser = Depends(authenticate_token)):
    return pc.log_trade(user.username, trade.ticker, trade.avg_price, trade.quantity, trade.fee, trade.timestamp)

@router.get("/api/v1/portfolio/trades")
def get_trade_history(user: AuthUser = Depends(authenticate_token),
                      page_no: int = Query(1, ge=1, description="Page number."),
                      page_size: int = Query(1, ge=1, description="Number of trades per page."),
                      ticker: str = Query(None, description="Filter trades by ticker symbol."),
                      sort_order: str = Query(None, description="Sort by ascending, descending, or none.")):
    return pc.get_trade_history(user.username, page_no, page_size, ticker, sort_order)

@router.get("/api/v1/portfolio/value")
def get_portfolio_historical_value(user: AuthUser = Depends(authenticate_token)):
    return pc.get_portfolio_historical_value(user.username)

@router.get("/api/v1/portfolio/forecast")
def get_monte_carlo_forecase(user: AuthUser = Depends(authenticate_token)):
    return pc.calculate_monte_carlo_simulation(user.username)
