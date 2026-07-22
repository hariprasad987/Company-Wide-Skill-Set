# Linux Administration Task

This task performs five basic server-administration operations:

1. Creates a local user named `skillmetrix` with a home directory and Bash shell.
2. Updates package indexes and installs available operating-system upgrades.
3. Installs Apache and enables it to start automatically.
4. Installs a custom terminal welcome message in `/etc/motd`.
5. Displays the server's IP addresses.

## Run

```bash
cd "4 - 7 yrs/Linux Administration"
chmod +x setup.sh
sudo ./setup.sh
```

The script is idempotent: running it again will reuse the existing user and Apache installation.

## Verify

```bash
id skillmetrix
systemctl is-enabled apache2
systemctl is-active apache2
curl http://localhost
cat /etc/motd
hostname -I
```

The new account is created without a password. An administrator can configure authentication later using the server's approved access policy.
