AI Text Analyzer – Production-like single-node DevOps stack using Terraform and Ansible

Live demo
http://46.224.191.124

Repository
https://github.com/presianrusinov/ansible-nginx-hardening

Overview

This project shows a complete, reproducible DevOps workflow for provisioning and configuring a production-style application stack on a single virtual machine. Everything can be rebuilt from scratch in a predictable way using infrastructure as code and configuration management.

Terraform is used to provision the infrastructure and firewall rules on Hetzner Cloud.
Ansible handles operating system configuration and application deployment on Rocky Linux 9.
Nginx serves the frontend and acts as a reverse proxy for the backend API.
Prometheus and exporters are included to provide real host metrics and basic observability.

The main goal of the project is to be realistic rather than over-engineered, and to demonstrate how a small but properly structured DevOps setup can look in practice.

Why Hetzner Cloud

The project was originally deployed on AWS EC2 and later migrated to Hetzner Cloud. The main reason for the migration was cost optimization and more predictable monthly pricing, while keeping exactly the same approach to infrastructure and configuration management.

Terraform is still responsible for provisioning infrastructure.
Ansible is still responsible for configuring the system and deploying the application.

The AWS version is kept in the repository as a historical reference.

High-level architecture

The entire application runs on a single virtual machine.

The frontend consists of static HTML, CSS and JavaScript files served by Nginx on port 80.

The backend is a Flask application served by Gunicorn and managed as a systemd service called ai-backend.service. It listens only on 127.0.0.1:5000 and is not exposed publicly. The main API endpoint is POST /api/analyze.

Nginx acts as a reverse proxy and forwards all requests under /api/ to the backend running on localhost.

The database is a local SQLite file located at /var/www/ai_project/ai.db.

Observability services are bound to localhost only. Prometheus runs on 127.0.0.1:9090, node_exporter on 127.0.0.1:9100, blackbox_exporter on 127.0.0.1:9115. Grafana on 127.0.0.1:3000 and Loki with Promtail can be enabled optionally.

Monitoring endpoints are intentionally not exposed to the public network.

Infrastructure provisioning with Terraform

Terraform provisions a Rocky Linux virtual machine on Hetzner Cloud.
Firewall rules allow inbound HTTP traffic on port 80.
SSH access is restricted to a single trusted public IP using Hetzner firewall rules.

The Hetzner API token is provided through an environment variable and is not stored anywhere in the repository.

Configuration management and deployment with Ansible

Ansible performs the full server setup and application deployment.

This includes installing and hardening Nginx, setting up the Python runtime and dependencies, deploying the backend application and configuring it as a systemd service using Gunicorn, deploying the frontend files to /usr/share/nginx/html, configuring the Nginx reverse proxy, and deploying the observability stack using Podman Quadlet units for Prometheus and exporters.

Verification and health checks

Application checks

Public entrypoint through Nginx
curl -I http://46.224.191.124

Backend service status on the VM
systemctl status ai-backend --no-pager

Verify that the backend listens only on localhost
ss -lntp | grep 127.0.0.1:5000 || true

Observability and metrics

Raw node_exporter metrics on the VM
curl -s http://127.0.0.1:9100/metrics
 | head

Prometheus readiness check
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9090/-/ready

Example Prometheus API queries
curl -s "http://127.0.0.1:9090/api/v1/query?query=up
"
curl -s "http://127.0.0.1:9090/api/v1/query?query=node_load1
"
curl -s "http://127.0.0.1:9090/api/v1/query?query=node_memory_MemAvailable_bytes
"
curl -s "http://127.0.0.1:9090/api/v1/query?query=rate(node_cpu_seconds_total[1m
])"

Security verification for monitoring endpoints

Confirm that monitoring services are bound to localhost only
ss -lntp | egrep "127.0.0.1:(9090|3000|3100|9100|9115)" || true

Database

The SQLite database file is located at
/var/www/ai_project/ai.db

Schema

CREATE TABLE IF NOT EXISTS analysis (
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT NOT NULL,
summary TEXT,
sentiment TEXT,
sentiment_score REAL,
keywords TEXT,
created_at TEXT
);

Future improvements

Add HTTPS with a real domain and TLS certificates.
Add a simple CI/CD pipeline for linting, testing and deployment.
Protect Grafana and Prometheus with basic authentication and reverse proxy access for demo use.
Expose backend application metrics using a Prometheus client and a /metrics endpoint.
Add alerting rules in Prometheus.

Author

Presiyan Rusinov
DevOps, Linux, Terraform, Ansible
Email: rusinovpresian@gmail.com

License

MIT License
