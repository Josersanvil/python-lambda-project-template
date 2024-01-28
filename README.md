# Python Lambda Deployment Template

This project provides a template for a containerised Python application that is designed to be deployed to an AWS Lambda function.

It contains a CD pipeline that builds the application, pushes it to an ECR repository and updates the Lambda function.

You must configure the following secrets and variables in your GitHub repository:

Secrets:

- AWS_IAM_ROLE_ARN: The ARN of an IAM role that has permission to push to the ECR repository and update the Lambda function
- AWS_ECR_REGISTRY: The URL of the ECR registry

Variables:

- AWS_LAMBDA_FUNCTION_NAME: The name of the Lambda function
- AWS_ECR_REPOSITORY: The name of the ECR repository
- AWS_REGION: The AWS region where the ECR repository and Lambda function are located

## Continue in Terraform

This project can be used with the following [Terraform](https://www.terraform.io/) configuration to deploy the Lambda function to AWS.

Just [install Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform), copy the following code into a file named `main.tf`, run `terraform init` and `terraform apply` to deploy the Lambda function. Push new changes to the main branch to update the Lambda function.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.16"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_ecr_repository" "app_repository" {
  name                 = "my-app"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_iam_role" "app_lambda_role" {
  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Principal = {
            Service = "lambda.amazonaws.com"
          }
          Action = "sts:AssumeRole"
        }
      ]
    }
  )

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
  ]
}

resource "aws_lambda_function" "app_lambda_function" {
  function_name = "my-app-function"
  role          = aws_iam_role.app_lambda_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app_repository.repository_url}:latest"
  timeout       = 300 # 5 minutes. Max is 15 minutes
  memory_size   = 256 # 256 MB. Max is 3008 MB (3 GB)

  environment {
    variables = {
      LAMBDA_LOG_LEVEL = "INFO"
    }
  }
}
```
