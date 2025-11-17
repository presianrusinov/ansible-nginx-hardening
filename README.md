DevOps Project — Ansible + Terraform + AWS + Nginx Hardening

This project demonstrates a complete Infrastructure as Code (IaC) workflow using Terraform, Ansible, and AWS.  
It automatically provisions an EC2 instance (Amazon Linux 2023), secures it with Nginx hardening, and deploys an HTML page served over HTTP and HTTPS.

---

  Live Demo
 Public URL: [http://63.177.86.189](http://63.177.86.189) 

(Hosted on AWS EC2, deployed automatically via Terraform + Ansible.)

---

 Project Overview

Stack used:
-  AWS EC2 (t2.micro, Free Tier)
-  Terraform — creates infrastructure
-  Ansible — configures and hardens Nginx
-  Security — SELinux, SSL, Permissions, `server_tokens off` - to be done and improved
-  Next phase: AI-generated “About Me” HTML page



 Project Structure



ansible-nginx-hardening/
├── ansible.cfg
├── inventory/
│ └── hosts
├── roles/
│ └── nginx_hardening/
│ ├── tasks/harden.yml
│ ├── handlers/main.yml
│ ├── defaults/
│ ├── vars/
│ └── templates/
├── site.yml
└── terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── provider.tf
├── terraform.tfvars
└── ansible-provision.sh




  Deployment Workflow

  Terraform Phase — Provision AWS Infrastructure


cd terraform
terraform init
terraform plan
terraform apply -auto-approve


Creates:

VPC, Subnet, Internet Gateway, Route Table

Security Group (ports 22, 80, 443)

EC2 instance (Amazon Linux 2023)

Output with the public IP

Example:

Outputs:
ec2_public_ip = "63.177.86.189"

 Ansible Phase — Configure and Harden Nginx

Edit inventory/hosts:

[aws_nginx]
63.177.86.189 ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/aws_key


Run:

ansible -i inventory/hosts aws_nginx -m ping
ansible-playbook -i inventory/hosts site.yml


This will:

Install and configure Nginx

Apply hardening (SSL, permissions, SELinux)

Deploy an example HTML page

 Verification

Access:
http://63.177.86.189

You should see:

Nginx is running on AWS EC2 (Amazon Linux 2023)
This page is automatically deployed via Ansible + Terraform.

 Screenshots
Description	Image
 Terraform Apply Success	

 Ansible Playbook Success	

 Working Nginx Page	
 Security Hardening Summary
Category	Action
Server Tokens	Disabled
File Permissions	0644 / 0755 enforced
SELinux Context	httpd_sys_content_t
SSL	Self-signed certificate
Root Path	/usr/share/nginx/html
 Next Phase (AI HTML “About Me” Page)

Next, the default landing page will be replaced with an AI-generated HTML “About Me” — a personalized web profile automatically deployed via Ansible.

 Author

Presian Rusinov
DevOps | Linux | Terraform | Ansible | AWS
 presianrusinov@gmail.com

 GitHub Repo : https://github.com/presianrusinov/ansible-nginx-hardening


 NOTE: Clarification on the use of ports and certificates

Port 80 is intentionally left open even though the service is also available over HTTPS on port 443. This is not a security weakness. Port 80 is required for the normal operation of the web server,
because it handles the automatic redirection from HTTP to HTTPS. Many clients and tools make their initial request over HTTP and expect to be redirected to a secure connection. Closing port 80 would 
result in unexpected behavior, failed requests, and in some cases complete loss of access.

Port 80 is also necessary for certificate validation mechanisms (such as ACME/Let’s Encrypt). The process of issuing or renewing certificates relies on HTTP access to verify domain ownership. If this port is closed, certificates cannot be issued or updated.

The “Not secure” message in the browser is expected when a self-signed certificate is used. This warning does not indicate a misconfiguration or an insecure setup; it simply means that the certificate was not issued by a publicly trusted authority. A real public certificate can be added if needed, but for demonstration, testing, or internal development, a self-signed certificate is completely acceptable.

These decisions follow standard practices for EC2-based web deployments and help ensure stable behavior, accessibility, and predictable operation of the service.

Keep consistent IP addressing in VirtualBox setups

🧠 Author

Maintainer: Presiyan Rusinov
License: MIT
