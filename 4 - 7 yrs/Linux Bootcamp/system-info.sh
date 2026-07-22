#!/usr/bin/env bash
set -euo pipefail

section() {
  printf '\n=== %s ===\n' "$1"
}

value_or_unknown() {
  local value="${1:-}"
  printf '%s\n' "${value:-Unknown}"
}

current_user="${SUDO_USER:-$(id -un)}"
user_record="$(getent passwd "${current_user}" || true)"
user_home="$(cut -d: -f6 <<<"${user_record}")"
user_shell="$(cut -d: -f7 <<<"${user_record}")"
os_name="$(. /etc/os-release 2>/dev/null && printf '%s' "${PRETTY_NAME:-Unknown}")"
cpu_model="$(lscpu 2>/dev/null | awk -F: '/Model name/ {sub(/^[[:space:]]+/, "", $2); print $2; exit}')"
primary_ip="$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{for (i=1; i<=NF; i++) if ($i == "src") {print $(i+1); exit}}')"

printf 'Linux System and User Information Report\n'
printf 'Generated: %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"

section "System Information"
printf 'Hostname       : %s\n' "$(hostname)"
printf 'Operating system: %s\n' "${os_name}"
printf 'Kernel         : %s\n' "$(uname -r)"
printf 'Architecture   : %s\n' "$(uname -m)"
printf 'CPU            : '
value_or_unknown "${cpu_model}"
printf 'CPU cores      : %s\n' "$(nproc)"
printf 'Uptime         : %s\n' "$(uptime -p)"
printf 'Primary IP     : '
value_or_unknown "${primary_ip}"

section "Memory Information"
free -h

section "Root Disk Usage"
df -h /

section "Current User Information"
printf 'Username       : %s\n' "${current_user}"
printf 'User ID        : %s\n' "$(id -u "${current_user}")"
printf 'Primary group  : %s\n' "$(id -gn "${current_user}")"
printf 'All groups     : %s\n' "$(id -Gn "${current_user}")"
printf 'Home directory : '
value_or_unknown "${user_home}"
printf 'Login shell    : '
value_or_unknown "${user_shell}"

section "Logged-in Sessions"
if ! who; then
  echo "Unable to read logged-in sessions."
fi

printf '\nReport complete.\n'
