from app.models.trades_models import Trade
from app.utils.exceptions import InvalidTradeError

class Portfolio():
    def __init__(self) -> None:
        self.assets = {}
        self.trades: list[Trade] = []

    def apply_trade(self, trade: Trade) -> None:
        ticker = trade.ticker

        if trade.quantity > 0: # Buy order
            self.assets[ticker] = self.assets.get(ticker, 0) + trade.quantity
        elif trade.quantity < 0: # Sell order
            if ticker not in self.assets:
                raise InvalidTradeError("Invalid trade!")

            new_quantity = self.assets[ticker] + trade.quantity

            if new_quantity < 0:
                raise InvalidTradeError("Invalid trade!")
            elif new_quantity == 0:
                del self.assets[ticker]
            else:
                self.assets[ticker] = new_quantity
        else:
            raise InvalidTradeError("Invalid trade!")

        self.trades.append(trade)

    def get_average_price(self) -> float:
        return 0.0
    
    def get_assets(self) -> dict:
        return self.assets

    def get_trades(self) -> dict:
        return self.trades
