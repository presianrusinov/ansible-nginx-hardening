variable "server_name" {
  type        = string
  description = "Name of the Hetzner server"
  default     = "nginx-hardening-1"
}

variable "server_type" {
  type        = string
  description = "Hetzner server type (e.g. cpx11, cpx21, cx22, ...)"
  default     = "cpx21"
}

variable "location" {
  type        = string
  description = "Hetzner location (fsn1, nbg1, hel1)"
  default     = "nbg1"
}

variable "ssh_key_name" {
  type        = string
  description = "Existing SSH key name in Hetzner Cloud"
  default     = "k8s-master-key"
}

variable "ssh_allowed_ipv4_cidrs" {
  type        = list(string)
  description = "IPv4 CIDRs allowed to SSH (22). Use your public IP /32."
  default     = ["0.0.0.0/0"]
}

variable "enable_http" {
  type        = bool
  description = "Allow inbound 80/tcp from anywhere"
  default     = true
}

variable "enable_https" {
  type        = bool
  description = "Allow inbound 443/tcp from anywhere"
  default     = true
}

variable "image" {
  type        = string
  description = "OS image name in Hetzner (e.g. rocky-9, rocky-10, alma-9, centos-stream-9)"
  default     = "rocky-9"
}

