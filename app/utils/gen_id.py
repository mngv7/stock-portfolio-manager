
def generate_trade_id(user_uuid: str, timestamp: str | int, ticker: str):
    return f"{user_uuid}#{timestamp}#{ticker}"

# default single portfolio accounts for now
def generate_portfolio_id(user_uuid: str, portfolio_no = "1"):
    return f"{user_uuid}#{portfolio_no}"
