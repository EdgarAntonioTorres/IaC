terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}

resource "aws_instance" "edgar_server_terr" {
  ami           = "ami-0cfde0ea8edd312d4"
  instance_type = "t3.micro"

  tags = {
    Name = "EdgarServerTerr"
  }

}

output "server_name" {
  value = aws_instance.edgar_server_terr.tags.Name
}