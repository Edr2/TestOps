# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr_block
  enable_dns_support = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "this" {
  cidr_block            = var.subnet_cidr_block
  vpc_id                = aws_vpc.this.id
  availability_zone     = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = false
}

output "vpc_id" {
  value = aws_vpc.this.id
}

output "subnet_id" {
  value = aws_subnet.this.id
}