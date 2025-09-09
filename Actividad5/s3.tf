resource "aws_s3_bucket" "jose_bucket" {
  bucket = "jose-terraform-bucket-012705"

  tags = {
    Name        = "joseBucketTerr"
    Environment = "dev"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.jose_bucket.bucket
}