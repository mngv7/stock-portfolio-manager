from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import portfolio_router as pr
from app.routes import users_router as ur
from app.routes import login_router as lr

origins = [
    "http://localhost:5173"
]

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
app.include_router(ur.router)
app.include_router(lr.router)

# TODO
# 1) CPU intensive task -- application uses a CPU intensive task.
# 2) CPU load testing -- generate a script or manual method to load down server.
# 3) Data types -- store at least two type of data.
# 4) Containerize the app -- bundle and store on AWS.
# 5) Deploy the container -- pull from AWS ECR and deploy on EC2 instance.
# 6) REST API
# 7) User login
