# provider "aws" {
#   region = "ap-southeast-2"
# }

# resource "aws_instance" "app_server" {
#   ami                    = "ami-04bd75753b33f7373"
#   subnet_id              = "subnet-04ca053dcbe5f49cc"
#   vpc_security_group_ids = ["sg-032bd1ff8cf77dbb9"]
#   instance_type          = "t3.micro"

#   iam_instance_profile = "CAB432-Instance-Role"

#   tags = {
#     Name         = "n11592931-assessment-2"
#     qut-username = "n11592931@qut.edu.au"
#     purpose      = "assessment-2"
#   }
# }

# resource "aws_cognito_user_pool" "app_user_pool" {
#   name = "n11592931-assessment-2-user-pool"

#   mfa_configuration = "OFF" # couldn't get around the permissions; configure manually :(

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_cognito_user_pool_client" "app_client_user_pool" {
#   name         = "n11592931-assessment-2-user-pool-client"
#   user_pool_id = aws_cognito_user_pool.app_user_pool.id

#   refresh_token_validity = 5 # in days
#   access_token_validity  = 1 # in hours
#   id_token_validity      = 1 # in hours

#   explicit_auth_flows = [
#     "ALLOW_USER_AUTH",
#     "ALLOW_USER_PASSWORD_AUTH",
#     "ALLOW_USER_SRP_AUTH",
#     "ALLOW_REFRESH_TOKEN_AUTH"
#   ]
# }

# resource "aws_route53_record" "public_dns_route_alias" {
#   name    = "portfoliomanager.cab432.com"
#   zone_id = "Z02680423BHWEVRU2JZDQ"
#   type    = "CNAME"

#   ttl = 300 # seconds

#   records = [aws_instance.app_server.public_dns]
# }

# resource "aws_dynamodb_table" "dynamodb_users_table" {
#   name           = "n11592931-users"
#   read_capacity  = 1
#   write_capacity = 1

#   hash_key  = "qut-username"
#   range_key = "uuid"

#   attribute {
#     name = "qut-username"
#     type = "S"
#   }

#   attribute {
#     name = "uuid"
#     type = "S"
#   }

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_dynamodb_table" "dynamodb_portfolios_table" {
#   name           = "n11592931-portfolios"
#   read_capacity  = 1
#   write_capacity = 1

#   hash_key  = "qut-username"
#   range_key = "portfolio_id"

#   attribute {
#     name = "qut-username"
#     type = "S"
#   }

#   attribute {
#     name = "portfolio_id"
#     type = "S"
#   }

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_dynamodb_table" "dynamodb_trades_table" {
#   name           = "n11592931-trades"
#   read_capacity  = 1
#   write_capacity = 1

#   hash_key  = "qut-username"
#   range_key = "trade_id"

#   attribute {
#     name = "qut-username"
#     type = "S"
#   }

#   attribute {
#     name = "trade_id"
#     type = "S"
#   }

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_s3_bucket" "s3_receipts_bucket" {
#   bucket = "n11592931-receipts"

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#     purpose      = "assessment-2"
#   }
# }

# resource "aws_s3_bucket_versioning" "receipts" {
#   bucket = aws_s3_bucket.s3_receipts_bucket.id

#   versioning_configuration {
#     status = "Disabled"
#   }
# }

# resource "aws_s3_bucket_server_side_encryption_configuration" "receipts" {
#   bucket = aws_s3_bucket.s3_receipts_bucket.id

#   rule {
#     apply_server_side_encryption_by_default {
#       sse_algorithm = "AES256"
#     }
#   }
# }

# resource "aws_elasticache_cluster" "memcached_cluster" {
#   cluster_id = "n11592931-assessment-3"

#   engine               = "memcached"
#   node_type            = "cache.t4g.micro"
#   parameter_group_name = "default.memcached1.6"
#   num_cache_nodes      = 1
#   subnet_group_name    = "cab432-subnets"

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_secretsmanager_secret" "cognito_secrets" {
#   name = "n11592931-cognito-secrets"

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_secretsmanager_secret_version" "user_pool_client_secret" {
#   secret_id     = "USERS_COGNITO_CLIENT_SECRET"
#   secret_string = aws_cognito_user_pool_client.app_client_user_pool.client_secret
# }

# resource "aws_ssm_parameter" "client_id_parameter" {
#   name  = "/n11592931/cognito/users/client_id"
#   type  = "String"
#   value = aws_cognito_user_pool_client.app_client_user_pool.client_secret

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_ssm_parameter" "user_pool_id_parameter" {
#   name  = "/n11592931/cognito/users/pool_id"
#   type  = "String"
#   value = aws_cognito_user_pool.app_user_pool.id

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }

# resource "aws_ssm_parameter" "memcached_endpoint_parameter" {
#   name  = "/n11592931/memcached/endpoint"
#   type  = "String"
#   value = aws_elasticache_cluster.memcached_cluster.configuration_endpoint

#   tags = {
#     qut-username = "n11592931@qut.edu.au"
#   }
# }
