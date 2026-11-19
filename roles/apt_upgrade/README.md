# iacker.fleet.apt_upgrade

## Entry point `main`

Upgrade packages, never reboot, report whether a reboot is needed.

- Runs an apt upgrade detached from the SSH session (async), keeps local config files.
- Sets the fact `apt_upgrade_reboot_required` for a later reboot role.

| Variable | Type | Default | Description |
|---|---|---|---|
| `apt_upgrade_type` | str | `"dist"` | Value passed to the `upgrade` option of ansible.builtin.apt. |
| `apt_upgrade_autoremove` | bool | `true` | Remove packages that are no longer needed. |
| `apt_upgrade_cache_valid_time` | int | `3600` | Skip `apt update` if the cache is younger than this (seconds). |
| `apt_upgrade_async` | int | `1800` | Maximum runtime of the detached upgrade (seconds). 0 runs it synchronously. |
| `apt_upgrade_poll` | int | `10` | Polling interval for the detached upgrade (seconds). |

See the [collection README](../../README.md) for complete playbooks.
