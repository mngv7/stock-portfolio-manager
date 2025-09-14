from fastapi import HTTPException
from app.utils.users import users
from app.models.trades_models import Trade
from app.models.portfolio_model import Portfolio

def get_portfolio_assets(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    return users[username].portfolio.get_assets()

def log_trade(username: str, ticker: str, avg_price: float, quantity: int, fee: float, timestamp: int):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    
    trade = Trade(ticker, avg_price, quantity, fee, timestamp)
    users[username].portfolio.apply_trade(trade)
    return {"message": "Trade successfully logged!"}

def get_trade_history(portfolio: Portfolio, page_no: int = 1, page_size: int = 10, ticker: str = None, sort_order: str = "desc"):    
    trades = portfolio.get_trades()

    if ticker:
        ticker = ticker.upper()
        trades: list[Trade] = trades.get(ticker, [])
    else:
        trades = [trade for trade_list in trades.values() for trade in trade_list]

    if len(trades) < 1:
        return []

    start_index = (page_no - 1) * page_size
    end_index = start_index + page_size

    trades_len = len(trades)
    trades = trades[start_index:end_index]
    
    if sort_order is None:
        return {"trade_list": trades,
                "length": trades_len}

    reverse = sort_order.lower() == "desc"
    return {"trade_list": sorted(trades, key=lambda t: t.timestamp, reverse=reverse),
            "length": trades_len}

def update_trade(username: str, trade_id: int, ticker: str, avg_price: float, quantity: int, fee: float, timestamp: int):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    
    updated_trade = users[username].portfolio.update_trade(trade_id, ticker, avg_price, quantity, fee, timestamp)
    if not updated_trade:
        raise HTTPException(status_code=404, detail=f"Trade with id {trade_id} not found")
    return {"message": "Trade successfully updated!", "trade": updated_trade}

def delete_trade(username: str, trade_id: int):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    
    success = users[username].portfolio.delete_trade(trade_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Trade with id {trade_id} not found")
    return None

def get_portfolio_historical_value(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail=f'{username} not found')
    
    return users[username].portfolio.get_portfolio_historical_value()

def calculate_monte_carlo_simulation(portfolio: Portfolio):
    return portfolio.monte_carlo_forecast()
