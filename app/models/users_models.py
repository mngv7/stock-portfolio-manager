from app.models.portfolio_model import Portfolio

class User:
    def __init__(self, email: str, username: str) -> None:
        self.email = email
        self.username = username
        self.portfolio = Portfolio(email)
