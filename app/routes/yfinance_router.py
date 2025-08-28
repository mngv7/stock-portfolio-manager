from fastapi import APIRouter, HTTPException, Query
import yfinance as yf

router = APIRouter()

@router.get("/price")
def get_current_price(ticker: str):
    pass
