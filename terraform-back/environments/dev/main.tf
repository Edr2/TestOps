# environments/dev/main.tf
# module "vpc" {
#   source     = "../../modules/vpc"
#   vpc_cidr_block = var.vpc_cidr_block
#   subnet_cidr_block = var.subnet_cidr_block
# }

module "eks" {
  source         = "../../modules/eks"
  cluster_name   = var.eks_cluster_name
  subnet_id      = module.vpc.subnet_id
  instance_type  = var.instance_type
}

# Reference the outputs from the eks module
output "eks_cluster_name" {
  value = module.eks.eks_cluster_name  # Referencing the output from the eks module
}

output "eks_cluster_endpoint" {
  value = module.eks.eks_cluster_endpoint  # Referencing the endpoint output from the eks module
}