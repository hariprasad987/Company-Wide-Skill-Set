#!/usr/bin/env bash
set -euo pipefail

readonly USER_NAME="${1:-skillmetrix}"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this script as root: sudo ./setup.sh" >&2
  exit 1
fi

echo "[1/5] Creating user: ${USER_NAME}"
if id "${USER_NAME}" >/dev/null 2>&1; then
  echo "User ${USER_NAME} already exists."
else
  useradd --create-home --shell /bin/bash "${USER_NAME}"
  echo "Created ${USER_NAME} with home directory /home/${USER_NAME}."
fi

echo "[2/5] Updating package indexes"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes

echo "[3/5] Installing and enabling Apache"
DEBIAN_FRONTEND=noninteractive apt-get install --yes apache2
systemctl enable --now apache2

echo "[4/5] Installing the terminal welcome message"
install --mode=0644 "${SCRIPT_DIR}/welcome-message.txt" /etc/motd

echo "[5/5] Server IP addresses"
hostname -I

echo
echo "Linux administration setup completed successfully."
