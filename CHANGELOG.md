# Changelog

## 1.0.0

First release.

- `apt_upgrade`: apt upgrade detached from the SSH session, exposes `apt_upgrade_reboot_required`.
- `k3s_rolling_reboot`: `preflight` entry point (all nodes Ready) and one-node reboot with cordon, optional drain, Ready wait, uncordon and a rescue that prints the recovery command.
- `podman_compose_update`: free-space guard, backups, pull, recreate (systemd unit or podman-compose), container health wait, prune, health and URL checks.
