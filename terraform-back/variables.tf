# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "eks_cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "vpc_cidr_block" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_block" {
  description = "List of CIDR blocks for subnets"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "Type of EC2 instance for worker nodes"
  type        = string
  default     = "t2.micro"
}