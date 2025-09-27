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
- **Two line description:** I/We implemented this very cool app that does Foo, Bar and Baz.
- **EC2 instance name or ID:**

------------------------------------------------

### Core - First data persistence service

- **AWS service name:** S3
- **What data is being stored?:** PDF files (trade receipts/statements).
- **Why is this service suited to this data?:** Large files are best suited to blob storage due to size restrictions on other services.
- **Why is are the other services used not suitable for this data?:**
- **Bucket/instance/table name:** n11592931-receipts
- **Video timestamp:**
- **Relevant files:**
    - /app/services/s3/*.py

### Core - Second data persistence service

- **AWS service name:**  DynamoDB
- **What data is being stored?:** User information, trades, and portfolios.
- **Why is this service suited to this data?:**
- **Why is are the other services used not suitable for this data?:**
- **Bucket/instance/table name:** n11592931-users, n11592931-trades, n11592931-portfolios
- **Video timestamp:**
- **Relevant files:**
    - app/services/dynamo/*.py

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
- **Video timestamp:**
- **Relevant files:**
    - /app/services/s3/receipts_bucket.py

### In-memory cache

- **ElastiCache instance name:** n11592931-assessment-2
- **What data is being cached?:** Historical prices for assets contained by a user's portfolio.
- **Why is this data likely to be accessed frequently?:** This data is fetched from Yahoo finance on page refresh to ensure user has the most up-to-date stock prices. These prices are then used for generating portfolio value graph and for Monte Carlo analysis. Caching these values (TTL 30 minutes) reduces yfinance API calls while balancing accurate prices. 
- **Video timestamp:**
- **Relevant files:**
    - /app/services/elasticache/memcached.py

### Core - Statelessness

- **What data is stored within your application that is not stored in cloud data services?:** There is no data stored in the server that isn't accessible from cloud data services. However, the client-side does store Monte carlo analysis output and tokens.
- **Why is this data not considered persistent state?:** Monte carlo analysis output can be recalculated from portfolio information (which is stored in the cloud). Tokens are session-based and do not requrie persistence.
- **How does your application ensure data consistency if the app suddenly stops?:** [eg. journal used to record data transactions before they are done.  A separate task scans the journal and corrects problems on startup and once every 5 minutes afterwards. ]
- **Relevant files:**
    -

### Graceful handling of persistent connections

- **Type of persistent connection and use:**
- **Method for handling lost connections:**
- **Relevant files:**
    -


### Core - Authentication with Cognito

- **User pool name:** n11592931-assessment-2-user-pool
- **How are authentication tokens handled by the client?:** [eg. Response to login request sets a cookie containing the token.]
- **Video timestamp:**
- **Relevant files:**
    - /app/services/cognito/cognito_services.py

### Cognito multi-factor authentication

- **What factors are used for authentication:** Email; a verification code is sent to the user's email.
- **Video timestamp:**
- **Relevant files:**
    - /app/services/cognito/cognito_services.py

### Cognito federated identities

- **Identity providers used:**
- **Video timestamp:**
- **Relevant files:**
    -

### Cognito groups

- **How are groups used to set permissions?:** Premium users gain access to portfolio analytical tools. A user can switch themselves to a premium user via the UI; in practice this would be blocked by a pay wall.
- **Video timestamp:**
- **Relevant files:**
    - 

### Core - DNS with Route53

- **Subdomain**: portfoliomanager.cab432.com
- **Video timestamp:**

### Parameter store

- **Parameter names:** n11592931/cognito/users/client_id, n11592931/cognito/users/pool_id, /n11592931/memcached/endpoint
- **Video timestamp:**
- **Relevant files:**
    - /app/services/parameter_store/parameter_store.py

### Secrets manager

- **Secrets names:** n11592931-cognito-secrets
- **Video timestamp:**
- **Relevant files:**
    - app/services/secrets/secrets_manager.py

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