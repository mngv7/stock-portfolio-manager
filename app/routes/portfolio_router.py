from fastapi import APIRouter, Depends, Query, Path
import app.controllers.portfolio_controller as pc
from app.utils.auth import AuthUser
from pydantic import BaseModel
from app.services.cognito.cognito_services import verify_jwt
from app.services.dynamo.trades_table import put_trade
from app.models.trades_models import Trade

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

# TODO
# Refactor the following to query the database with the sub identifier

@router.get("/api/v1/portfolio/assets")
def get_portfolio_assets(user = Depends(verify_jwt)):
    pass
    # return pc.get_portfolio_assets(user.username)

@router.post("/api/v1/portfolio/trades", status_code=201)
def log_trade(trade: TradeRequest, user_uuid = Depends(verify_jwt)):
    trade_object = Trade(trade.ticker,
                         trade.avg_price,
                         trade.quantity,
                         trade.fee,
                         trade.timestamp)
    return put_trade(user_uuid["sub"], trade_object)

@router.get("/api/v1/portfolio/trades")
def get_trade_history(user = Depends(verify_jwt),
                      page_no: int = Query(1, ge=1, description="Page number."),
                      page_size: int = Query(1, ge=1, description="Number of trades per page."),
                      ticker: str = Query(None, description="Filter trades by ticker symbol."),
                      sort_order: str = Query(None, description="Sort by ascending, descending, or none.")):
    pass
    # return pc.get_trade_history(user.username, page_no, page_size, ticker, sort_order)

@router.put("/api/v1/portfolio/trades/{trade_id}")
def update_trade(trade_id: int, trade: TradeRequest, user = Depends(verify_jwt)):
    pass
    # return pc.update_trade(user.username, trade_id, trade.ticker, trade.avg_price, trade.quantity, trade.fee, trade.timestamp)

@router.delete("/api/v1/portfolio/trades/{trade_id}", status_code=204)
def delete_trade(trade_id: int, user = Depends(verify_jwt)):
    pass
    # return pc.delete_trade(user.username, trade_id)

@router.get("/api/v1/portfolio/value")
def get_portfolio_historical_value(user = Depends(verify_jwt)):
    pass
    # return pc.get_portfolio_historical_value(user.username)

@router.get("/api/v1/portfolio/forecast")
def get_monte_carlo_forecase(user = Depends(verify_jwt)):
    pass
    # return pc.calculate_monte_carlo_simulation(user.username)
