from app.models.portfolio_model import Portfolio

class User:
    def __init__(self, email: str, username: str, password: str) -> None:
        self.email = email
        self.username = username
        self.password = password
        self.portfolio = Portfolio()
