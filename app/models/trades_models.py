import time

class Trade():
    def __init__(self, ticker: str, avg_price: float, quantity: int, fee: float, timestamp: float = None) -> None:
        assert quantity != 0
        self.ticker = ticker
        self.avg_price = avg_price
        self.quantity = quantity
        self.fee = fee
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()
