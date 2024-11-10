# environments/dev/terraform.tfvars
aws_region      = "eu-central-1"
eks_cluster_name = "my-eks-cluster-dev"
vpc_cidr_block  = "10.0.0.0/16"
subnet_cidr_block = "10.0.1.0/24"
instance_type    = "t2.micro"