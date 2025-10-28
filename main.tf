// ------------------- Lambda -------------------
resource "aws_lambda_function" "n11592931_queue_length_asg_metric" {
  function_name = "n11592931-queue-length-ASG-metric"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  role          = "arn:aws:iam::901444280953:role/CAB432-Lambda-Role"
  timeout       = 30
  memory_size   = 128

  filename         = "${path.module}/lambda/index.py"

  environment {
    variables = {
      QUEUE_NAME       = "n11592931-monte-carlo-tasks"
      ASG_NAME         = aws_autoscaling_group.asg.name
      METRIC_NAMESPACE = "StockPortfolioManager/SQSBacklog"
      METRIC_NAME      = "BacklogPerInstance"
    }
  }
}

// ------------------- EventBridge -------------------
resource "aws_cloudwatch_event_rule" "bpi_publisher" {
  name                = "periodic-bpi-checker"
  schedule_expression = "rate(1 minute)"
}

resource "aws_cloudwatch_event_target" "bpi_lambda" {
  rule = aws_cloudwatch_event_rule.bpi_publisher.name
  arn  = aws_lambda_function.n11592931_queue_length_asg_metric.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.n11592931_queue_length_asg_metric.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.bpi_publisher.arn
}

// ------------------- Auto Scaling Group -------------------

resource "aws_autoscaling_group" "asg" {
  name                      = "n11592931-monte-carlo-scaler"
  min_size                  = 1
  max_size                  = 3
  desired_capacity          = 1
  health_check_type         = "EC2"
  health_check_grace_period = 300

  launch_template {
    id      = "lt-0d8fdf1d5d281e860"
    version = "$Latest"
  }

  vpc_zone_identifier = [
    "subnet-075811427d5564cf9",
    "subnet-05a3b8177138c8b14",
    "subnet-04ca053dcbe5f49cc"
  ]

  tag {
    key                 = "purpose"
    value               = "assessment 3"
    propagate_at_launch = true
  }

  tag {
    key                 = "qut-username"
    value               = "n11592931@qut.edu.au"
    propagate_at_launch = true
  }

  tag {
    key                 = "Name"
    value               = "monte-carlo-worker"
    propagate_at_launch = true
  }
}

// ------------------- ASG Scaling Policy -------------------

resource "aws_autoscaling_policy" "bpi_target" {
  name                   = "n11592931-bpi-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.asg.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    customized_metric_specification {
      metric_name = "BacklogPerInstance"
      namespace   = "StockPortfolioManager/SQSBacklog"
      statistic   = "Average"
    }

    target_value     = 1
    disable_scale_in = false
  }
}

// ------------------- SQS -------------------

data "aws_sqs_queue" "monte_carlo_tasks" {
  name = "n11592931-monte-carlo-tasks"
}

data "aws_sqs_queue" "monte_carlo_dlq" {
  name = "n11592931-monte-carlo-tasks-dlq"
}
// ------------------- Cloud Front -------------------


resource "aws_s3_bucket" "frontend" {
  bucket = "n11592931-static-front-end"

  tags = {
    Name = "Portfolio Manager Frontend"
  }
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "frontend_public" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend.arn}/*"
      }
    ]
  })
}

provider "aws" {
  alias  = "useast1"
  region = "us-east-1"
}

data "aws_acm_certificate" "cab432" {
  provider = aws.useast1
  domain   = "portfoliomanager.cab432.com"
  statuses = ["ISSUED"]
}

resource "aws_cloudfront_distribution" "frontend" {
  enabled             = true
  is_ipv6_enabled     = false
  comment             = "Portfolio Manager Static Site"
  default_root_object = "index.html"
  price_class         = "PriceClass_All"

  aliases = ["portfoliomanager.cab432.com"]

  origin {
    domain_name = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id   = "S3-n11592931-static-front-end"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-n11592931-static-front-end"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600  # 1 hour
    max_ttl                = 86400 # 1 day
    compress               = false
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = data.aws_acm_certificate.cab432.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  tags = {
    Environment = "production"
  }
}

resource "aws_api_gateway_rest_api" "n11592931_assessment_3_api_gateway" {
  name        = "n11592931-assessment-3"
  description = "REST API for auth and api microservices"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}