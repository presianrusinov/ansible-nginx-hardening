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

Keep consistent IP addressing in VirtualBox setups

🧠 Author

Maintainer: Presiyan Rusinov
License: MIT
