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
