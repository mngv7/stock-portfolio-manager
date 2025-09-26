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

- **AWS service name:**  S3
- **What data is being stored?:** PDF files (trade receipts/statements).
- **Why is this service suited to this data?:** Large files are best suited to blob storage due to size restrictions on other services.
- **Why is are the other services used not suitable for this data?:**
- **Bucket/instance/table name:** n11592931-receipts
- **Video timestamp:**
- **Relevant files:**
    -

### Core - Second data persistence service

- **AWS service name:**  DynamoDB
- **What data is being stored?:** User information, trades, and portfolios.
- **Why is this service suited to this data?:**
- **Why is are the other services used not suitable for this data?:**
- **Bucket/instance/table name:** n11592931-users, n11592931-trades, n11592931-portfolios
- **Video timestamp:**
- **Relevant files:**
    -

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
    -

### In-memory cache

- **ElastiCache instance name:** n11592931-assessment-2
- **What data is being cached?:** Historical prices for assets contained by a user's portfolio.
- **Why is this data likely to be accessed frequently?:**
- **Video timestamp:**
- **Relevant files:**
    -

### Core - Statelessness

- **What data is stored within your application that is not stored in cloud data services?:** [eg. intermediate video files that have been transcoded but not stabilised]
- **Why is this data not considered persistent state?:** [eg. intermediate files can be recreated from source if they are lost]
- **How does your application ensure data consistency if the app suddenly stops?:** [eg. journal used to record data transactions before they are done.  A separate task scans the journal and corrects problems on startup and once every 5 minutes afterwards. ]
- **Relevant files:**
    -

### Graceful handling of persistent connections

- **Type of persistent connection and use:** [eg. server-side-events for progress reporting]
- **Method for handling lost connections:** [eg. client responds to lost connection by reconnecting and indicating loss of connection to user until connection is re-established ]
- **Relevant files:**
    -


### Core - Authentication with Cognito

- **User pool name:** n11592931-assessment-2-user-pool
- **How are authentication tokens handled by the client?:** [eg. Response to login request sets a cookie containing the token.]
- **Video timestamp:**
- **Relevant files:**
    -

### Cognito multi-factor authentication

- **What factors are used for authentication:** Email code.
- **Video timestamp:**
- **Relevant files:**
    -

### Cognito federated identities

- **Identity providers used:**
- **Video timestamp:**
- **Relevant files:**
    -

### Cognito groups

- **How are groups used to set permissions?:** Premium users gain access to portfolio analytical tools.
- **Video timestamp:**
- **Relevant files:**
    -

### Core - DNS with Route53

- **Subdomain**:  portfoliomanager.cab432.com
- **Video timestamp:**

### Parameter store

- **Parameter names:** [eg. n1234567/base_url]
- **Video timestamp:**
- **Relevant files:**
    -

### Secrets manager

- **Secrets names:** [eg. n1234567-youtube-api-key]
- **Video timestamp:**
- **Relevant files:**
    -

### Infrastructure as code

- **Technology used:** TerraForm
- **Services deployed:**
- **Video timestamp:**
- **Relevant files:**
    -

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