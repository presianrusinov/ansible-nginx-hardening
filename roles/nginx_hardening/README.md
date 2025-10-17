# Nginx Hardening Role

This Ansible role installs and hardens the Nginx web server to improve security and ensure consistent configuration across environments.



# Features

- Installs Nginx automatically (if not already installed)
- Disables `server_tokens` to hide the Nginx version
- Enforces secure file and directory permissions
- Generates a **self-signed SSL certificate**
- Enables **HTTPS** (TLS 1.2 / 1.3) with strong ciphers
- Includes an automatic **handler to restart Nginx** on configuration changes



# Role Structure



roles/nginx_hardening/
├── defaults/
├── files/
├── handlers/
│ └── main.yml
├── tasks/
│ ├── main.yml
│ └── harden.yml
├── templates/
├── vars/
└── README.md


# Usage

Include this role in your playbook as shown below:

yaml:

- name: Apply Nginx Hardening
  hosts: target
  become: yes
  roles:
    - nginx_hardening


Then run:

ansible-playbook -i inventory/hosts site.yml

 Tasks Overview:

tasks/main.yml	- Installs and starts Nginx, includes hardening tasks
tasks/harden.yml - Implements server tokens, permissions, and SSL configuration
handlers/main.yml - Restarts Nginx after configuration changes
 Notes

Designed for RHEL-based systems (RHEL, CentOS, Rocky Linux, AlmaLinux)

Can be adapted for Debian/Ubuntu by changing the package module to apt

Ideal for integration in CI/CD pipelines or Terraform provisioning

Follows idempotent Ansible practices
