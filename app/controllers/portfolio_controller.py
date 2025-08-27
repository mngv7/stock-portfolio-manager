from fastapi import APIRouter, HTTPException
from app.utils.users import users
from app.models.trades_models import Trade

router = APIRouter()

def get_portfolio_assets(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    return users[username].portfolio.get_assets()

def log_trade(username: str, ticker: str, avg_price: float, quantity: int, fee: float):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    
    trade = Trade(ticker, avg_price, quantity, fee)
    users[username].portfolio.apply_trade(trade)
    return {"message": "Trade successfully logged!"}

def get_trade_history(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    
    return users[username].portfolio.get_trades()