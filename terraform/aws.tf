variable "aws-region" {
  type = string
  default = "us-east-1"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  backend "s3" {
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.aws-region
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

locals {
    deter_name = "nuagecron-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
}