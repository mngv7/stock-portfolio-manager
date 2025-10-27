from app.models.trades_models import Trade
from app.models.portfolio_model import Portfolio

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