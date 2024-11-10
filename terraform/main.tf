provider "aws" {
  region = "eu-central-1"
}

# EKS Cluster
resource "aws_eks_cluster" "dev" {
  name     = "dev-eks-cluster"
  role_arn = aws_iam_role.eks_cluster.arn

  vpc_config {
    # TODO create subnets/vpc in tf too
    # Use the first default subnet ID in the current region
    subnet_ids = ["subnet-0d645796520a60745", "subnet-09b9899f6919c558e"]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_iam_role_policy_attachment.eks_service_policy,
  ]
}

# EKS Node Group
resource "aws_eks_node_group" "dev" {
  cluster_name    = aws_eks_cluster.dev.name
  node_group_name = "dev-node-group"
  node_role_arn    = aws_iam_role.eks_nodes.arn

  # Use the first default subnet ID in the current region
  subnet_ids = ["subnet-0d645796520a60745"]

  instance_types = ["t2.micro"]
  capacity_type  = "ON_DEMAND"
  disk_size      = 20

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_nodes_policy,
    aws_iam_role_policy_attachment.eks_workers_policy,
  ]
}

# IAM Role for EKS Cluster
resource "aws_iam_role" "eks_cluster" {
  name = "eks-cluster-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

# IAM Role for EKS Nodes
resource "aws_iam_role" "eks_nodes" {
  name = "eks-node-group-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

# Attach EKS-related policies to the IAM roles
resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

resource "aws_iam_role_policy_attachment" "eks_service_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.eks_cluster.name
}

resource "aws_iam_role_policy_attachment" "eks_nodes_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_workers_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_nodes.name
}

# Outputs
output "cluster_name" {
  value       = aws_eks_cluster.dev.name
  description = "EKS Cluster Name"
}

output "cluster_endpoint" {
  value       = aws_eks_cluster.dev.endpoint
  description = "EKS Cluster Endpoint"
}