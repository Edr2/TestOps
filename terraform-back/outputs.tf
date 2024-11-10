# module "eks" {
#   source        = "./modules/eks" # Adjust the path to your `eks` module location
#   cluster_name  = var.eks_cluster_name
#   subnet_id     = module.vpc.subnet_id
#   instance_type = var.instance_type
# }

# output "eks_cluster_name" {
#   value = module.eks.eks_cluster_name
# }

# output "eks_cluster_endpoint" {
#   value = module.eks.eks_cluster_endpoint
# }
