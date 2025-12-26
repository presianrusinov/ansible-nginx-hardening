output "server_ipv4" {
  value = hcloud_server.nginx.ipv4_address
}

output "server_ipv6" {
  value = hcloud_server.nginx.ipv6_address
}

output "server_name" {
  value = hcloud_server.nginx.name
}

output "image_name" {
  value = var.image
}

