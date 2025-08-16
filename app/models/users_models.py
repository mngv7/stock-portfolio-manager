from models.portfolio_model import Portfolio

class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.portfolio = Portfolio()
