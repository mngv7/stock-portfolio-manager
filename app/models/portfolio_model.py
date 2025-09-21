from app.models.trades_models import Trade
from app.utils.exceptions import InvalidTradeError
import numpy as np
import pandas as pd
from datetime import datetime
from app.services.elasticache.memcached import CachedTicker

class Portfolio():
    def __init__(self, user_uuid: str, portfolio_no: str) -> None:
        self.user_uuid = user_uuid
        self.portfolio_no = portfolio_no
        self.portfolio_id = f"{user_uuid}#{portfolio_no}"

        self.assets: dict[str, int] = {}
        self.trades: dict[str, list[Trade]] = {}

    def apply_trade(self, trade: Trade) -> None:
        ticker = trade.ticker

        if trade.quantity > 0:  # Buy order
            self.assets[ticker] = self.assets.get(ticker, 0) + trade.quantity
        elif trade.quantity < 0:  # Sell order
            if ticker not in self.assets:
                raise InvalidTradeError("Invalid trade! Cannot sell what you don't own.")

            new_quantity = self.assets[ticker] + trade.quantity
            if new_quantity < 0:
                raise InvalidTradeError("Invalid trade! Not enough shares to sell.")
            elif new_quantity == 0:
                del self.assets[ticker]
            else:
                self.assets[ticker] = new_quantity
        else:
            raise InvalidTradeError("Invalid trade! Quantity cannot be zero.")

        if ticker not in self.trades:
            self.trades[ticker] = []
        
        self.trades[ticker].append(trade)


    # def update_trade(self, trade_id: int, ticker: str, avg_price: float, quantity: int, fee: float, timestamp: int):
    #     if trade_id not in self.trade_index:
    #         return None
    #     trade = self.trade_index[trade_id]
    #     trade.ticker = ticker
    #     trade.avg_price = avg_price
    #     trade.quantity = quantity
    #     trade.fee = fee
    #     trade.timestamp = timestamp
    #     return {
    #         "id": trade_id,
    #         "ticker": ticker,
    #         "avg_price": avg_price,
    #         "quantity": quantity,
    #         "fee": fee,
    #         "timestamp": timestamp
    #     }

    # def delete_trade(self, trade_id: int):
    #     if trade_id not in self.trade_index:
    #         return False
    #     trade = self.trade_index.pop(trade_id)
    #     if trade.ticker in self.trades:
    #         self.trades[trade.ticker] = [t for t in self.trades[trade.ticker] if getattr(t, "id", None) != trade_id]
    #     return True

    def get_portfolio_weights(self) -> dict:
        result = {}
        total_value = 0
        for ticker, amount in self.assets.items():
            try:
                asset = CachedTicker(ticker)
            except:
                print("Not a valid ticker.")
            asset_price = asset.info['currentPrice']
            asset_volume = asset_price * amount
            total_value += asset_volume
            result[ticker] = asset_volume

        for ticker, volume in result.items():
            result[ticker] = volume / total_value

        return result

    def monte_carlo_forecast(self, simulations=50000, time_frame="1y", days=252) -> dict:
        if len(self.assets.keys()) < 2:
            return {}

        portfolio_weights = np.array([self.get_portfolio_weights()[ticker] for ticker in self.assets.keys()])
        cov_matrix = self.get_portfolio_cov()
        mean_return = {}

        for ticker in self.assets.keys():
            asset = CachedTicker(ticker)
            historical_prices = asset.history(period=time_frame)['Close']
            returns = historical_prices.pct_change().dropna()
            mean_return[ticker] = returns.mean() * 252

        mean_vector = np.array([mean_return[ticker] for ticker in self.assets.keys()])
        chol_decomp = np.linalg.cholesky(cov_matrix)
        portfolio_returns = np.zeros(simulations)

        for sim in range(simulations):
            portfolio_value = 1.0
            for _ in range(days):
                rand_normals = np.random.normal(size=len(self.assets))
                correlated_returns = mean_vector / days + (chol_decomp @ rand_normals) / np.sqrt(days)
                portfolio_daily_return = correlated_returns @ portfolio_weights
                portfolio_value *= (1 + portfolio_daily_return)
            portfolio_returns[sim] = portfolio_value - 1

        expected_return = np.mean(portfolio_returns)
        volatility = np.std(portfolio_returns)
        percentile_5 = np.percentile(portfolio_returns, 5)
        percentile_95 = np.percentile(portfolio_returns, 95)
        var_95 = np.percentile(portfolio_returns, 5)

        return {
            "expected_return": float(expected_return),
            "volatility": float(volatility),
            "5th_percentile": float(percentile_5),
            "95th_percentile": float(percentile_95),
            "VaR_95": float(var_95),
            "distribution": portfolio_returns.tolist()
        }

    def get_portfolio_cov(self):
        returns_dict = {}
        for ticker in self.assets.keys():
            asset = CachedTicker(ticker)
            historical_prices = asset.history(period="1y")['Close']
            returns_dict[ticker] = historical_prices.pct_change().dropna()
        returns_df = pd.DataFrame(returns_dict)
        cov_matrix = np.cov(returns_df, rowvar=False)
        return cov_matrix

    def get_portfolio_historical_value(self):
        portfolio_value = pd.Series(dtype=float)

        for ticker in self.assets.keys():
            ticker = ticker.upper()
            stock = CachedTicker(ticker)
            trade_history = self.trades[ticker]

            trade_history.sort(key=lambda t: t.timestamp)
            # trade history here are strings
            start_dt = datetime.fromtimestamp(trade_history[0].timestamp)
            end_dt = datetime.now()
            data = stock.history(
                start=start_dt.strftime("%Y-%m-%d"),
                end=end_dt.strftime("%Y-%m-%d"),
                interval="1d"
            )

            prices = data["Close"]
            quantities = pd.Series(0, index=prices.index)

            for trade in trade_history:
                trade_date = datetime.fromtimestamp(trade.timestamp).date()
                quantities.loc[quantities.index.date >= trade_date] += trade.quantity

            ticker_value = prices * quantities
            portfolio_value = portfolio_value.add(ticker_value, fill_value=0)

        return portfolio_value

    def get_assets(self) -> dict:
        return self.assets

    def get_trades(self) -> dict[str, list[Trade]]:
        return self.trades
