terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configuración del provider AWS
provider "aws" {
  region = "us-east-2"
}

# Instancia EC2 
resource "aws_instance" "edgar_server_terr" {
  ami           = "ami-0cfde0ea8edd312d4"
  instance_type = "t3.micro"

  tags = {
    Name = "EdgarServerTerr"
  }
}

# Bucket en S3
resource "aws_s3_bucket" "edgar_bucket" {
  bucket = "edgar-terraform-bucket-012705"

  tags = {
    Name        = "EdgarBucketTerr"
    Environment = "dev"
  }
}

# Output de la instancia
output "server_name" {
  value = aws_instance.edgar_server_terr.tags.Name
}

# Output del bucket
output "bucket_name" {
  value = aws_s3_bucket.edgar_bucket.bucket
}