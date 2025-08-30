Assignment 1 - REST API Project - Response to Criteria
================================================

Overview
------------------------------------------------

- **Name:** Zackariya Taylor
- **Student number:** n11592931
- **Application name:** Stock Portfolio Manager
- **Two line description:** This REST API provides users with tools to log and track trades. This API can also be used to run simulations on a user's portfolio.


Core criteria
------------------------------------------------

### Containerise the app

- **ECR Repository name:** n11592931-stock-portfolio-manager
- **Video timestamp:**
- **Relevant files:**
    - /Dockerfile

### Deploy the container

- **EC2 instance ID:**
- **Video timestamp:**

### User login

- **One line description:** Hard coded username and passwords, JWT and localStorage() used for session management.
- **Video timestamp:**
- **Relevant files:**
    - /app/utils/users.py

### REST API

- **One line description:** REST API with endpoints as nouns and HTTP methods (GET, POST), and appropriate status codes.
- **Video timestamp:**
- **Relevant files:**
    - /app/controllers/login_controller.py
    - /app/controllers/portfolio_controller.py
    - /app/controllers/users_controller.py
    - /app/routes/auth_router.py
    - /app/routes/login_router.py
    - /app/routes/portfolio_router.py
    - /app/routes/users_router.py
    - /app/routes/yfinance_router.py

### Data types

- **One line description:** Data stored for users, portfolios, and trades.
- **Video timestamp:**
- **Relevant files:**
    - /app/models/portfolio_model.py
    - /app/models/trades_models.py
    - /app/models/users_models.py

#### First kind

- **One line description:** Each user owns a portfolio which contains a log of assets and trades.
- **Type:** Structured
- **Rationale:** Portfolios are structured stateful aggregations of user holdings. They track current asset quantities (as well as methods to compute portfolio weights, forecasting etc.). As each user has a distinct portfolio, there are ideally no concurrency issues, so no ACID guarantees are necessary.
- **Video timestamp:**
- **Relevant files:**
    - /app/models/portfolio_model.py

#### Second kind

- **One line description:** Portfolios comprise of trade objects (containing metadata on every trade).
- **Type:** Structured
- **Rationale:** Trade objects are lightweight structured records (historical events/transactions), containing metadata for each trade, such as ticker, price, quantity, fee, timestamp, etc. Trades can also be used to audit ownership. These do not require ACID transactions but must be stored reliably for portfolio calculations.
- **Video timestamp:**
- **Relevant files:**
    - /app/models/trades_models.py 

### CPU intensive task

 **One line description:** Runs a Monte Carlo simulation with Geometric Brownian motion to forecast potential portfolio performance.
- **Video timestamp:** 
- **Relevant files:**
    - /app/models/portfolio_model.py
    - /app/routes/portfolio_router.py
    - /app/controllers/portfolio_controller.py

### CPU load testing

 **One line description:** Python script to generate multiple requests for '/portfolio/forecast' endpoint.
- **Video timestamp:** 
- **Relevant files:**
    - /load_tester.py

Additional criteria
------------------------------------------------

### Extensive REST API features

- **One line description:** Not attempted
- **Video timestamp:**
- **Relevant files:**
    - 

### External API(s)

- **One line description:** Yahoo Finance API used to fetch stock prices and historical data to perform Monte Carlo simulations and plot graphs.
- **Video timestamp:**
- **Relevant files:**
    - /app/routes/yfinance_router.py
    - /app/models/portfolio_model.py

### Additional types of data

- **One line description:** Not attempted
- **Video timestamp:**
- **Relevant files:**
    - 

### Custom processing

- **One line description:** Monte Carlo with Geometric Brownian Motion implemented manually, with helper functions such as get_portfolio_cov(), and other data manipulation within get_portfolio_historical_value. See https://www.investopedia.com/articles/07/montecarlo.asp for simulation theory.
- **Video timestamp:**
- **Relevant files:**
    - /app/models/portfolio_model.py

### Infrastructure as code

- **One line description:** Not attempted
- **Video timestamp:**
- **Relevant files:**
    - 

### Web client

- **One line description:** Web client with login page and dashboard to access API endpoints. Charts and graphs included.
- **Video timestamp:**
- **Relevant files:**
    - /client/src/*

### Upon request

- **One line description:** Not attempted
- **Video timestamp:**
- **Relevant files:**
    - 