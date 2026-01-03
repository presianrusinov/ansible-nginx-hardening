# AI Text Analyzer – Terraform and Ansible deployment on Hetzner Cloud

Live demo:
http://46.224.191.124

Repository:
https://github.com/presianrusinov/ansible-nginx-hardening


Overview

This project demonstrates a complete end-to-end DevOps workflow for provisioning, configuring and deploying a small web application in the cloud using Infrastructure as Code and configuration management.

The environment is fully reproducible. A single command sequence can provision the server, configure the operating system, deploy the application stack and make it available publicly.

The project focuses on realistic DevOps practices rather than production-grade complexity.


Why Hetzner Cloud (migration from AWS)

The project was initially deployed on AWS EC2. It was later migrated to Hetzner Cloud for cost optimization and predictable monthly expenses while preserving the same technical workflow and deployment logic.

The migration did not change the architecture or tooling philosophy:
Terraform is still responsible for infrastructure provisioning.
Ansible is still responsible for configuration and application deployment.

The current live demo runs on Hetzner Cloud, while the AWS implementation is kept as a historical reference in the project’s evolution.


Operating system and environment

The server runs Rocky Linux 9, chosen to stay close to a Red Hat Enterprise Linux-like environment with systemd and SELinux enabled.

A dedicated ansible user is used for configuration management with passwordless sudo access.


High-level architecture

The application runs entirely on a single virtual machine.

Nginx serves static frontend files over HTTP on port 80.

Nginx also acts as a reverse proxy for backend API requests under /api/.

The backend is served using Gunicorn instead of the Flask development server.

Gunicorn was chosen to provide a production-grade WSGI server with proper process management, improved reliability and better integration with systemd.

The backend service is hardened using multiple systemd security directives and validated using systemd-analyze security.

The backend persists results in a local SQLite database.

The backend is not exposed publicly and can only be accessed through Nginx.


Infrastructure provisioning (Terraform)

Terraform is used to provision the infrastructure on Hetzner Cloud.

The Terraform layer creates:
A virtual machine using a Rocky Linux image
Firewall rules allowing HTTP access
Firewall rules restricting SSH access to a single public IP address

The Hetzner API token is provided through an environment variable and is not stored in the repository.

After provisioning, Terraform outputs the public IP address which is then used by Ansible.


Configuration management and deployment (Ansible)

Ansible connects to the server using the ansible user and performs the full configuration.

Ansible installs and configures:
Nginx
Python 3 and required dependencies
The backend application
A systemd service for the backend
The static frontend files
The Nginx reverse proxy configuration

When the playbook completes, the application is immediately available.


Frontend

The frontend consists of static HTML, CSS and JavaScript files.

The files are deployed to:
/usr/share/nginx/html

The frontend communicates with the backend using HTTP requests to:
/api/


Backend

The backend is a Flask application that performs basic text analysis.

It provides an API endpoint:
POST /api/analyze

The backend runs as a systemd service named:
ai-backend.service

It listens only on:
127.0.0.1:5000

This ensures that the backend cannot be accessed directly from the internet.


Database (SQLite)

The project uses SQLite for data persistence.

Database file location:
/var/www/ai_project/ai.db

SQLite was chosen because it is lightweight, serverless and suitable for a single-instance deployment.

The database is created automatically if it does not exist.


Database schema

The backend initializes the database with the following table:

CREATE TABLE IF NOT EXISTS analysis (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT NOT NULL,
  summary TEXT,
  sentiment TEXT,
  sentiment_score REAL,
  keywords TEXT,
  created_at TEXT
);


How the backend uses the database

Each API request stores a record containing:
The original input text
The generated summary
The sentiment label and score
Extracted keywords
A timestamp

The database allows basic inspection and validation of backend behavior.


Security notes

The security configuration is intentionally kept simple to maintain clarity and reproducibility.

SSH access is restricted to a single public IP address using Hetzner firewall rules.

The backend is not exposed publicly and is accessible only through Nginx.

No sensitive data is processed.

HTTPS is not enabled because the project uses a raw IP address without a domain name.


Future improvements

Possible future extensions include:
Enabling HTTPS once a domain is available
Improving backend error handling
Enhancing frontend visualization
Containerizing the backend
Migrating the database to a managed service
Adding CI/CD automation
Adding monitoring and alerting for the backend service


Author

Presiyan Rusinov
DevOps / Linux / Terraform / Ansible

Email: rusinovpresian@gmail.com

GitHub repository:
https://github.com/presianrusinov/ansible-nginx-hardening

License: MIT
