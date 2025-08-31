from fastapi import APIRouter, Depends, Query, Path
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

@router.post("/api/v1/portfolio/trades", status_code=201)
def log_trade(trade: TradeRequest, user: AuthUser = Depends(authenticate_token)):
    return pc.log_trade(user.username, trade.ticker, trade.avg_price, trade.quantity, trade.fee, trade.timestamp)

@router.get("/api/v1/portfolio/trades")
def get_trade_history(user: AuthUser = Depends(authenticate_token),
                      page_no: int = Query(1, ge=1, description="Page number."),
                      page_size: int = Query(1, ge=1, description="Number of trades per page."),
                      ticker: str = Query(None, description="Filter trades by ticker symbol."),
                      sort_order: str = Query(None, description="Sort by ascending, descending, or none.")):
    return pc.get_trade_history(user.username, page_no, page_size, ticker, sort_order)

@router.put("/api/v1/portfolio/trades/{trade_id}")
def update_trade(trade_id: int, trade: TradeRequest, user: AuthUser = Depends(authenticate_token)):
    return pc.update_trade(user.username, trade_id, trade.ticker, trade.avg_price, trade.quantity, trade.fee, trade.timestamp)

@router.delete("/api/v1/portfolio/trades/{trade_id}", status_code=204)
def delete_trade(trade_id: int, user: AuthUser = Depends(authenticate_token)):
    return pc.delete_trade(user.username, trade_id)

@router.get("/api/v1/portfolio/value")
def get_portfolio_historical_value(user: AuthUser = Depends(authenticate_token)):
    return pc.get_portfolio_historical_value(user.username)

@router.get("/api/v1/portfolio/forecast")
def get_monte_carlo_forecase(user: AuthUser = Depends(authenticate_token)):
    return pc.calculate_monte_carlo_simulation(user.username)
