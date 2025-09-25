provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_instance" "app_server" {
  ami                    = "ami-04bd75753b33f7373"
  subnet_id              = "subnet-04ca053dcbe5f49cc"
  vpc_security_group_ids = ["sg-032bd1ff8cf77dbb9"]
  instance_type          = "t3.micro"
  tags = {
    Name         = "n11592931-assessmnet-2"
    qut-username = "n11592931@qut.edu.au"
    purpose      = "assessment-2"
  }
}

resource "aws_cognito_user_pool" "app_user_pool" {
  name = "n11592931-assessment-2-user-pool"

  mfa_configuration = "OFF"  # TerraForm does not support email MFA; configure manually

  tags = {
    qut-username = "n11592931@qut.edu.au"
  }
}


resource "aws_cognito_user_pool_client" "app_client_user_pool" {
  name         = "n11592931-assessment-2-user-pool-client"
  user_pool_id = aws_cognito_user_pool.app_user_pool.id

  refresh_token_validity = 5 # in days
  access_token_validity  = 1 # in hours
  id_token_validity      = 1 # in hours

  explicit_auth_flows = [
    "ALLOW_USER_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
}
