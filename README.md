DevOps Project: Terraform, Ansible, AWS EC2 and Nginx

This project demonstrates a complete end-to-end workflow for deploying an application in the cloud using Infrastructure as Code. The environment is built on AWS EC2 (Amazon Linux 2023) and is fully configured through Terraform and Ansible. On top of the basic Nginx deployment, the project now includes a lightweight AI-style text analysis service written in Python (Flask), along with a custom frontend interface.

The project was created with the goal of practicing a realistic DevOps deployment pipeline: provisioning, configuration management, service automation, and application delivery.

Application Overview

The application consists of two parts: a static frontend served by Nginx and a small backend service running on Flask. The backend performs simple text analysis (summary, sentiment, keywords) and stores results in a SQLite database. Everything is deployed on a single EC2 instance.
The frontend communicates with the backend through a thin API layer, and both components are provisioned and configured automatically through Ansible.

Infrastructure Workflow

Terraform creates the full AWS environment:
VPC, subnet, route table, internet gateway, security group and the EC2 instance. After the instance is online, its public IP address is used for the Ansible inventory.

Ansible then connects to the instance and performs the required setup steps:
installation and configuration of Nginx, deployment of the frontend files, installation of Python packages, configuration of the Flask backend service and creation of a systemd unit that runs the backend automatically.

Once the playbook finishes, both the frontend and backend become available immediately.

Project Layout

The repository contains two main sections: one for Terraform and one for Ansible. The Terraform folder includes the EC2 setup, networking and outputs. The Ansible folder contains the roles for the frontend and backend, the site playbook and the inventory.

The backend files (Python scripts, schema and requirements) are placed inside the backend role, which copies them to the server and configures the service. The frontend role keeps the static HTML, CSS and JavaScript files which get deployed to the Nginx root directory.

Security Notes

The current security configuration is kept intentionally simple so the project can remain easy to understand and reproduce on any new instance.
Port 80 is open publicly and allows direct HTTP access. This is not ideal for production but is acceptable for a small experimental project where ease of access is more important than strict hardening. The service does not process anything sensitive, and the demonstrational nature of the project makes strict HTTPS enforcement unnecessary at this stage.

The backend API listens only on localhost and is not exposed directly to the internet. The only externally accessible part is the frontend served by Nginx. For a real production system, traffic would be forced through HTTPS with a valid certificate and security groups would be restricted further. Here, the setup is left intentionally open just enough to allow simple testing without additional obstacles.

This approach makes it easy to rebuild or re-run the entire environment without dealing with certificate trust issues or complex access restrictions. The decisions above will be revisited later if the project is expanded into a more advanced version.

Future Work

The next steps are refining the backend logic, improving the frontend design, adding history visualisation of previous analyses and considering full HTTPS reverse proxy integration once a domain name is available. If needed, the backend can also be containerised or moved behind a load balancer as part of a future scaling demonstration.

Author

Presiyan Rusinov
DevOps | Linux | Terraform | Ansible | AWS
rusinovpresian@gmail.com

GitHub repository: https://github.com/presianrusinov/ansible-nginx-hardening


 Author

Maintainer: Presiyan Rusinov
License: MIT
