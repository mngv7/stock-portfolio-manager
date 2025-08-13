from fastapi import FastAPI
from app.routes import portfolio_router as pr
from app.routes import trades_router as tr
from app.routes import users_router as ur
from app.routes import login_router as lr

app = FastAPI(
    title="Stock Portfolio Tracker API",
    description="Tool for managing a stock portfolio and forecasting prices.",
    version="0.0.1"
)

app.include_router(pr.router)
app.include_router(tr.router)
app.include_router(ur.router)
app.include_router(lr.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
