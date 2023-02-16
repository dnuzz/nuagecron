resource "null_resource" "build_requirements" {

 provisioner "local-exec" {
    
    command = "poetry export --without-hashes -f requirements.txt -o requirements.txt --with-credentials"
  }
}

resource "aws_s3_bucket" "storage" {
    bucket = local.deter_name
}

locals {
  lambda_storage_prefix = "lambda_functions/"
}

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  depends_on = [
    null_resource.build_requirements
  ]

  function_name = "terraform-test-lambda"
  description   = "My awesome lambda function"
  handler       = "nuagecron.adapters.aws.lambdas.tick_lambda_handler"
  runtime       = "python3.8"


  source_path = [
    "../servicename.json",
    {
        pip_requirements = "../requirements.txt",
    },
    {
    path             = "../nuagecron",
    prefix_in_zip    = "nuagecron/"
    },
    {
    path             = "../api",
    prefix_in_zip    = "api/"
    }
  ]
  store_on_s3 = true
  build_in_docker = true

  docker_file = "../Dockerfile"
  docker_image = "lambci/lambda:build-python3.8"

  s3_bucket = aws_s3_bucket.storage.bucket
  s3_prefix = local.lambda_storage_prefix

  tags = {
    Name = "tf-nuagecron"
  }
}

resource "aws_lambda_function" "temp_test_tick" {
  function_name = "temp-test-tick"

  role = module.lambda_function.lambda_role_arn

  handler = "nuagecron.adapters.aws.lambdas.tick_lambda_handler"
  runtime = "python3.8"

  s3_bucket = module.lambda_function.s3_object.bucket
  s3_key = module.lambda_function.s3_object.key
}
