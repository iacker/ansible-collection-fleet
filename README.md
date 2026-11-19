# iacker.fleet

[![CI](https://github.com/iacker/ansible-collection-fleet/actions/workflows/ci.yml/badge.svg)](https://github.com/iacker/ansible-collection-fleet/actions/workflows/ci.yml)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-iacker.fleet-blue?logo=ansible)](https://galaxy.ansible.com/ui/repo/published/iacker/fleet/)

Rolling maintenance for small fleets, written for a real one: a three-node k3s
cluster reached over Tailscale and a cloud VM running a podman-compose stack
that other people use during the day.

Each role does one job and refuses to continue when the situation is unsafe.

| Role | What it does | Main guard |
|---|---|---|
| `apt_upgrade` | Upgrades packages, never reboots, sets `apt_upgrade_reboot_required` | apt runs detached (`async`), so an upgrade of the VPN that carries SSH cannot kill dpkg halfway |
| `k3s_rolling_reboot` | `preflight`: every node Ready. `main`: cordon, reboot, wait Ready, uncordon | stops the whole run on the first failure and prints the exact uncordon command |
| `podman_compose_update` | Backs up, pulls, recreates, waits for healthy containers, prunes, checks URLs | refuses to pull without enough free disk |

## Install

```bash
ansible-galaxy collection install iacker.fleet
```

Requires ansible-core 2.18+ and `kubectl` on the controller for `k3s_rolling_reboot`.

## Rolling OS update of a k3s cluster

```yaml
- name: Preflight
  hosts: localhost
  gather_facts: false
  tasks:
    - ansible.builtin.include_role:
        name: iacker.fleet.k3s_rolling_reboot
        tasks_from: preflight

- name: Agents first, one at a time
  hosts: k3s_agents
  serial: 1
  any_errors_fatal: true
  become: true
  roles:
    - iacker.fleet.apt_upgrade
    - iacker.fleet.k3s_rolling_reboot

- name: Server last
  hosts: k3s_server
  serial: 1
  any_errors_fatal: true
  become: true
  roles:
    - iacker.fleet.apt_upgrade
    - iacker.fleet.k3s_rolling_reboot
```

Nodes reboot only when the OS asks for it (`/var/run/reboot-required`), or with
`-e k3s_rolling_reboot_force=true`. Set `k3s_rolling_reboot_node_name` in
`host_vars` when the Kubernetes node name differs from the inventory name.

**Why drain is off by default.** On a small cluster, draining the big node pushes
its heavy pods onto the smallest one, which then thrashes, and `local-path`
volumes cannot move anyway. Cordon plus a two-minute reboot lets pods restart in
place. Turn it on with `k3s_rolling_reboot_drain: true` when you have the headroom.

## Updating a podman-compose stack

```yaml
- hosts: app_vm
  roles:
    - role: iacker.fleet.podman_compose_update
      vars:
        podman_compose_update_project_dir: /home/app/stack
        podman_compose_update_project_name: app
        podman_compose_update_systemd_unit: app-stack
        podman_compose_update_backup_files: [compose.yml, .env, /home/app/data/app.db]
        podman_compose_update_expected_containers: [app_web_1, app_api_1]
        podman_compose_update_health_commands:
          - { name: api, cmd: "podman exec app_web_1 curl -fsS http://api:8080/health", expect: ok }
        podman_compose_update_url_checks:
          - { url: "https://app.example.com/", status: [200] }
```

Back up the database of any service that migrates its schema on start: without
it, rolling back to the old image is not possible.

## Testing

CI runs `ansible-lint` (production profile), `ansible-test sanity`, builds the
collection, and runs `apt_upgrade` and `podman_compose_update` for real on a
GitHub runner. `k3s_rolling_reboot` is exercised in check mode on a live
cluster before each release; rebooting CI runners is not possible.

## License

MIT
