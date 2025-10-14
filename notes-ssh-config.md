# 🚨 Issue Summary

Error:
Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password)


Context:
- The `ansible` user existed on the target node
- The public key was copied manually but authentication still failed
- SSH worked for `root`, but not for `ansible`

---

## 🔍 Root Cause Analysis

1. Key mismatch —  
   The wrong (private) key was copied instead of the public one.

2. Wrong file permissions —  
   `/home/ansible/.ssh` and `authorized_keys` were owned by `root`, not `ansible`.

3. SELinux and mode restrictions —  
   Permissions needed to be exactly:
   
   chmod 700 /home/ansible/.ssh
   chmod 600 /home/ansible/.ssh/authorized_keys
   chown -R ansible:ansible /home/ansible/.ssh
SSH Agent Forwarding confusion —
PuTTY and Pageant were not correctly configured initially, causing missing key forwarding.

🧭 Fix Steps
On control node, check which key is used:


ls -l ~/.ssh/
ssh-keygen -lf ~/.ssh/id_rsa.pub
Copy the public key to target node:


ssh-copy-id ansible@192.168.118.11
Verify permissions:



chmod 700 /home/ansible/.ssh
chmod 600 /home/ansible/.ssh/authorized_keys
chown -R ansible:ansible /home/ansible/.ssh
Test connection manually:



ssh ansible@192.168.118.11
✅ Result: passwordless login successful.

💡 Lessons Learned
Always verify which key is public/private before copying

File ownership is critical for SSH key authentication

In VirtualBox setups, NAT + Host-only can cause confusion in connectivity tests

Documenting every issue saves hours of troubleshooting

🧾 References
How to configure key-based authentication for SSH:
https://www.redhat.com/en/blog/key-based-authentication-ssh

Ansible Best Practices- Privilege Escalation :
https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_privilege_escalation.html

