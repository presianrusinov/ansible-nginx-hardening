DevOps Project: Terraform, Ansible, AWS EC2 and Nginx

Live demo:
http://63.177.86.189/

This project demonstrates a complete end-to-end DevOps workflow for deploying a small application in the cloud using Infrastructure as Code. The environment is built on AWS EC2 (Amazon Linux 2023) and is fully automated using Terraform and Ansible. In addition to the Nginx setup, the project includes a lightweight text-analysis backend written in Python (Flask) and a custom frontend interface.

The purpose of the project is to practice a realistic DevOps deployment pipeline: provisioning, configuration management, service automation and application delivery.

Application Overview

The application consists of two main components:

Frontend – static HTML/CSS/JS served by Nginx.

Backend – a small Flask service that performs text analysis (summary, sentiment, keywords) using the VADER sentiment library.

Database – each analysis is stored locally in a SQLite file.

Everything runs on a single EC2 instance. The frontend communicates with the backend through a small internal API, and both components are fully deployed and configured using Ansible.

Infrastructure Workflow
Terraform layer

Terraform provisions the full AWS environment:

VPC

Subnet

Route table

Internet gateway

Security group

EC2 instance

After Terraform finishes, it outputs the public IP address of the instance. This same IP is then used inside the Ansible inventory.

Ansible layer

Once the EC2 machine is reachable by SSH, Ansible performs the remaining setup:

installs and configures Nginx

deploys the static frontend files

installs Python and the required dependencies

deploys the Flask backend

creates and enables a systemd service for the backend

prepares the directory structure and database file

When the playbook completes, both the frontend and backend are live.

Project Layout

The repository is structured into two main directories:

terraform/ — contains the EC2 definition, networking, outputs and variables

ansible/ — contains roles for the frontend and backend, the site playbook and the inventory

The backend role includes:

app.py (Flask application)

requirements.txt

systemd unit file

database initialization logic

The frontend role contains the static UI files which are copied to the Nginx root directory.

Database Details (SQLite)

The project uses a simple SQLite database (ai.db) to store every text analysis performed by the backend.

Location
/var/www/ai_project/ai.db


SQLite is used because it is lightweight, serverless and perfectly suitable for a small single-instance application.

Schema

The database initializes itself when the backend starts for the first time.
The table structure is:

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

The POST request /api/analyze receives JSON input:

{ "text": "..." }


The backend runs its analysis:

sentiment via VADER

keyword extraction

summary

The result is stored as a new entry in the analysis table.

The API returns the full dataset back to the frontend, including the generated fields and timestamp.

Checking stored results

On the EC2 instance:

sqlite3 /var/www/ai_project/ai.db "SELECT * FROM analysis;"

Why SQLite for this project

It keeps the setup simple and reproducible. No additional services are required (no MySQL/PostgreSQL), and the entire environment can be recreated from scratch instantly by running Terraform + Ansible again.
For a larger or multi-instance deployment, the backend could easily be adapted to use RDS or another external database.

Security Notes

The security configuration is intentionally kept minimal so the project can remain easy to rebuild and test:

Port 80 is open publicly for easier access during testing.

The backend listens only on localhost and is not directly exposed.

No sensitive data is processed.

For a production environment, HTTPS termination, stricter security groups and more advanced hardening would be required.
Here, the priority is simplicity and clarity of the workflow.

Future Work

Planned improvements:

enhance the backend logic and error handling

polish the frontend UI

add visualization for stored analyses

enable HTTPS once a domain is available

containerize the backend or run it behind a load balancer

optionally migrate the database to RDS

Author

Presiyan Rusinov
DevOps | Linux | Terraform | Ansible | AWS
rusinovpresian@gmail.com

GitHub repository:
https://github.com/presianrusinov/ansible-nginx-hardening

License: MIT
