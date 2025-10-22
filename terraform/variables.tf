variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
}

variable "public_key_path" {
  description = "Path to your local public key"
  type        = string
  default     = "~/.ssh/aws_key.pub"
}

variable "project_name" {
  description = "Project tag for resources"
  type        = string
  default     = "ai-devops-nginx"
}

variable "ami_id" {
  description = "AMI ID for Amazon Linux 2023 in selected region"
  type        = string
}

