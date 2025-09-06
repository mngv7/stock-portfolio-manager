from app.models.portfolio_model import Portfolio

class User:
    def __init__(self, email: str, username: str, password_hashed: str) -> None:
        self.email = email
        self.username = username
        self.password_hashed = password_hashed
        self.portfolio = Portfolio(email)
