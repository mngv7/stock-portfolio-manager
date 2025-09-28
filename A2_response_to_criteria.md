Assignment 2 - Cloud Services Exercises - Response to Criteria
================================================

Instructions
------------------------------------------------
- Keep this file named A2_response_to_criteria.md, do not change the name
- Upload this file along with your code in the root directory of your project
- Upload this file in the current Markdown format (.md extension)
- Do not delete or rearrange sections.  If you did not attempt a criterion, leave it blank
- Text inside [ ] like [eg. S3 ] are examples and should be removed


Overview
------------------------------------------------

- **Name:** Zackariya Taylor
- **Student number:** n11592931
- **Partner name (if applicable):**
- **Application name:** Stock Portfolio Manager
- **Two line description:** This application allows users to keep track of their portfolio by logging investments and storing trade receipts or other relevant PDF files. The app also includes portfolio analysis tools which is available only to premium users.
- **EC2 instance name or ID:** i-06255798a94baa207

------------------------------------------------

### Core - First data persistence service

- **AWS service name:** S3
- **What data is being stored?:** PDF files (trade receipts/statements).
- **Why is this service suited to this data?:** S3 is best for storing PDF files due to its scalability; allowing the app to store a large numer of PDFs, and high durability; ensure trade documents are intact. It is optimized for large amounts of unstructured data objects (PDF binaries), alternate services may not be as cost effective or efficient.
- **Why is are the other services used not suitable for this data?:** Other persistent services are designed for different use cases. EBS is intended for EC2 volumes rather than long-term file storage. RDS and DynamoDB are designed for structured data, not large files. EFS is like a standard filesystem, not necessary for this application as we only need to fetch PDFs by keys, rather than having an organised file structure. These alternate services are less efficient for PDF storage; S3 is the best use for this application.
- **Bucket/instance/table name:** n11592931-receipts
- **Video timestamp:** 0:00
- **Relevant files:**
    - /app/services/s3/receipts_bucket.py
    - /app/routes/portfolio_router.py

### Core - Second data persistence service

- **AWS service name:**  DynamoDB
- **What data is being stored?:** User information, trades, and portfolios.
- **Why is this service suited to this data?:**
- **Why is are the other services used not suitable for this data?:**
- **Bucket/instance/table name:** n11592931-users, n11592931-trades, n11592931-portfolios
- **Video timestamp:** 0:30
- **Relevant files:**
    - /app/services/dynamo/portfolios_table.py
    - /app/services/dynamo/users_table.py
    - /app/services/dynamo/trades_table.py
    - /app/routes/portfolio_router.py

### Third data service

- **AWS service name:**
- **What data is being stored?:**
- **Why is this service suited to this data?:**
- **Why is are the other services used not suitable for this data?:**
- **Bucket/instance/table name:**
- **Video timestamp:**
- **Relevant files:**
    -

### S3 Pre-signed URLs

- **S3 Bucket names:** n11592931-receipts
- **Video timestamp:** 0:48
- **Relevant files:**
    - /app/services/s3/receipts_bucket.py
    - /app/routes/portfolio_router.py

### In-memory cache

- **ElastiCache instance name:** n11592931-assessment-2
- **What data is being cached?:** Historical prices for assets contained by a user's portfolio.
- **Why is this data likely to be accessed frequently?:** This data is fetched from Yahoo finance on page refresh to ensure user has the most up-to-date stock prices. These prices are then used for generating portfolio value graph and for Monte Carlo analysis. Caching these values (TTL 30 minutes) reduces yfinance API calls while balancing accurate prices. 
- **Video timestamp:** 1:16
- **Relevant files:**
    - /app/services/elasticache/memcached.py
    - /app/models/portfolio_model.py

### Core - Statelessness

- **What data is stored within your application that is not stored in cloud data services?:** There is no data stored in the server that isn't accessible from cloud data services. However, the client-side does store Monte carlo analysis output and tokens.
- **Why is this data not considered persistent state?:** Monte carlo analysis output can be recalculated from portfolio information (which is stored in the cloud). Tokens are session-based and do not requrie persistence.
- **How does your application ensure data consistency if the app suddenly stops?:** The app does not inherently handle data consistency, it uses DynamoDB as a single source of truth.
- **Relevant files:**
    -

### Graceful handling of persistent connections

- **Type of persistent connection and use:**
- **Method for handling lost connections:**
- **Relevant files:**
    -


### Core - Authentication with Cognito

- **User pool name:** n11592931-assessment-2-user-pool
- **How are authentication tokens handled by the client?:** The client stores the ID Token in localstorage() once the user satisfies MFA. Once this token is set, it is sent to the backend to verify various endpoints. The client also uses the ID token to restrict navigation to various sites of the application.
- **Video timestamp:** 1:53
- **Relevant files:**
    - /app/services/cognito/cognito_services.py
    - /app/routes/auth_router.py
    - /client/src/pages/Login/LoginChallengeContainer.tsx

### Cognito multi-factor authentication

- **What factors are used for authentication:** Password and email code; once the user logs in with the correct password, they are prompted to enter the code sent to the email they signed up with.
- **Video timestamp:** 2:36
- **Relevant files:**
    - /app/services/cognito/cognito_services.py
    - /app/routes/auth_router.py

### Cognito federated identities

- **Identity providers used:**
- **Video timestamp:**
- **Relevant files:**
    -

### Cognito groups

- **How are groups used to set permissions?:** Premium users gain access to portfolio analytical tools. A user can switch themselves to a premium user via the UI; in practice this would be blocked by a pay wall.
- **Video timestamp:** 2:55
- **Relevant files:**
    - /app/services/cognito/cognito_services.py
    - /client/src/pages/Dashboard/Analysis.tsx

### Core - DNS with Route53

- **Subdomain**: portfoliomanager.cab432.com
- **Video timestamp:** 3:51

### Parameter store

- **Parameter names:** n11592931/cognito/users/client_id, n11592931/cognito/users/pool_id, /n11592931/memcached/endpoint
- **Video timestamp:** 4:08
- **Relevant files:**
    - /app/services/parameter_store/parameter_store.py
    - /app/services/cognito/cognito_services.py
    - /app/services/elasticache/memcached.py

### Secrets manager

- **Secrets names:** n11592931-cognito-secrets
- **Video timestamp:** 4:47
- **Relevant files:**
    - /app/services/secrets/secrets_manager.py
    - /app/services/cognito/cognito_services.py

### Infrastructure as code

- **Technology used:** TerraForm
- **Services deployed:** EC2, Cognito, Route53, DynamoDB, S3, ElastiCache (memcached), Secrets Manager, Parameter Store
- **Video timestamp:**
- **Relevant files:**
    - /main.tf
    - /terraform.tf

### Other (with prior approval only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
    -

### Other (with prior permission only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
    -
