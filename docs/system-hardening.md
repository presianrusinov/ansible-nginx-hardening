### systemd Service Hardening

The AI backend is secured using systemd sandboxing features managed via Ansible.
Hardening is applied through a drop-in override to ensure:

- Principle of least privilege
- Reduced kernel and filesystem attack surface
- Automatic service recovery on failure

Security posture is validated using `systemd-analyze security`.

