#  Ansible Nginx Hardening Project

This project demonstrates a complete Ansible automation setup for Nginx installation and service hardening between two RHEL 9.6 virtual machines._

---

# 🧱 Infrastructure Overview

| Role         | Hostname       | OS       | IP Address     | Purpose          |
|---------------|----------------|-----------|----------------|------------------|
| Control Node | control-node   | RHEL 9.6 | 192.168.118.10 | Runs Ansible     |
| Target Node  | target-node    | RHEL 9.6 | 192.168.118.11 | Managed by Ansible |

VirtualBox configuration:
- Adapter 1 (NAT): Internet access (Red Hat subscription, package updates)  
- Adapter 2 (Host-only): Internal LAN for Ansible control

---

# Step 0 — Environment Preparation

# Control Node
- Installed `ansible-core 2.14.18`
- Registered via `subscription-manager`
- Verified SSH and network connectivity (`ping 192.168.118.11`)
- Configured passwordless SSH to target node

# Target Node
- Registered to Red Hat
- Created `ansible` user (non-root best practice)
- Allowed SSH access for the ansible user

---

## 🔐 SSH Configuration

Passwordless SSH setup between control and target nodes.

#bash
# On target node:
drwx------ ansible ansible /home/ansible/.ssh
-rw------- ansible ansible /home/ansible/.ssh/authorized_keys

Validation Test
[root@control-node ~]# ssh ansible@192.168.118.11
Last login: ...
[ansible@target-node ~]$


✅ Result: connection works without password

📁 Project Structure
ansible-nginx-hardening/
├── ansible.cfg
├── inventory/
│   └── hosts
├── roles/
│   └── nginx_hardening/
│       └── tasks/
│           └── main.yml
└── site.yml

⚙️ Step 1 — Verify Connectivity
ansible -i inventory/hosts target -m ping


Expected output:

192.168.118.11 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

🚀 Step 2 — Deploy & Harden Nginx
roles/nginx_hardening/tasks/main.yml
- name: Install Nginx
  ansible.builtin.dnf:
    name: nginx
    state: present

- name: Ensure Nginx is enabled and running
  ansible.builtin.service:
    name: nginx
    enabled: true
    state: started

site.yml
- name: Nginx Hardening Playbook
  hosts: target
  become: true
  roles:
    - nginx_hardening

🧪 Step 3 — Run the Playbook
ansible-playbook site.yml


Expected output:

PLAY RECAP *********************************************************************
192.168.118.11 : ok=3  changed=2  unreachable=0  failed=0

🔎 Step 4 — Verification
systemctl status nginx
ss -tuln | grep 80


✅ Expected: Nginx active & listening on port 80

🧩 Next Steps

Disable default index page

Harden /etc/nginx permissions

Add server_tokens off

Configure SSL/TLS certificates

 Notes:

Both VMs run RHEL 9.6

Control Node runs Ansible 2.14.18

SSH authentication fixed (see notes.md for troubleshooting)

Lessons learned:

Always verify permissions and ownership

Test SSH manually before automation

Avoid using root for remote connections

Keep consistent IP addressing in VirtualBox setups

🧠 Author

Maintainer: Presiyan Rusinov
License: MIT
