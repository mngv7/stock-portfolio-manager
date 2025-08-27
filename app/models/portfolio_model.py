from app.models.trades_models import Trade
from app.utils.exceptions import InvalidTradeError
import yfinance as yf
import numpy as np
import pandas as pd

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

    def get_portfolio_weights(self) -> dict:
        result = {}
        total_value = 0
        for ticker, amount in self.assets.items():
            try:
                asset = yf.Ticker(ticker)
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
        # Get portfolio weights
        portfolio_weights = np.array([self.get_portfolio_weights()[ticker] for ticker in self.assets.keys()])
        
        # Covariance and mean returns
        cov_matrix = self.get_portfolio_cov()
        mean_return = {}

        # Collect mean annual returns
        for ticker, _ in self.assets.items():
            asset = yf.Ticker(ticker)
            historical_prices = asset.history(period=time_frame)['Close']
            returns = historical_prices.pct_change().dropna()
            mean_return_annual = returns.mean() * 252
            mean_return[ticker] = mean_return_annual

        mean_vector = np.array([mean_return[ticker] for ticker in self.assets.keys()])
        
        # Precompute Cholesky for correlated random draws
        chol_decomp = np.linalg.cholesky(cov_matrix)

        # Store portfolio simulations
        portfolio_returns = np.zeros(simulations)

        for sim in range(simulations):
            portfolio_value = 1.0  # start normalized
            for day in range(days):
                # Generate correlated random shocks
                rand_normals = np.random.normal(size=len(self.assets))
                correlated_returns = mean_vector / days + (chol_decomp @ rand_normals) / np.sqrt(days)
                
                # Portfolio daily return
                portfolio_daily_return = correlated_returns @ portfolio_weights
                
                # Compound portfolio value
                portfolio_value *= (1 + portfolio_daily_return)

            # Store final portfolio value
            portfolio_returns[sim] = portfolio_value - 1  # total return over horizon

        # Compute statistics
        expected_return = np.mean(portfolio_returns)
        volatility = np.std(portfolio_returns)
        percentile_5 = np.percentile(portfolio_returns, 5)
        percentile_95 = np.percentile(portfolio_returns, 95)
        var_95 = np.percentile(portfolio_returns, 5)

        return {
            "expected_return": expected_return,
            "volatility": volatility,
            "5th_percentile": percentile_5,
            "95th_percentile": percentile_95,
            "VaR_95": var_95,
            "distribution": portfolio_returns
        }

    def get_portfolio_cov(self):
        returns_dict = {}

        for ticker, _ in self.assets.items():
            asset = yf.Ticker(ticker)
            historical_prices = asset.history(period="1y")['Close']
            returns = historical_prices.pct_change().dropna()
            returns_dict[ticker] = returns

        returns_df = pd.DataFrame(returns_dict)
        cov_matrix = np.cov(returns_df, rowvar=False)
        return cov_matrix
    
    def get_assets(self) -> dict:
        return self.assets

    def get_trades(self) -> list[Trade]:
        return self.trades
