from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import portfolio_router as pr
from app.routes import auth_router as ar
from app.routes import util_router as ur

origins = ["*"]

app = FastAPI(
    title="Stock Portfolio Tracker API",
    description="Tool for managing a stock portfolio and forecasting prices.",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pr.router)
app.include_router(ar.router)
app.include_router(ur.router)
