# iacker.fleet.k3s_rolling_reboot

## Entry point `main`

Reboot one k3s node safely (cordon, optional drain, Ready wait, uncordon).

- Meant to run with `serial: 1` and `any_errors_fatal: true`.
- kubectl commands are delegated to the controller.
- On failure the play stops and prints the exact uncordon command.

| Variable | Type | Default | Description |
|---|---|---|---|
| `k3s_rolling_reboot_kubectl` | str | `"kubectl"` | kubectl command on the controller, for example `kubectl --context prod`. |
| `k3s_rolling_reboot_node_name` | str | `"{{ inventory_hostname }}"` | Kubernetes node name, when it differs from the inventory name. |
| `k3s_rolling_reboot_needed` | bool | `"{{ apt_upgrade_reboot_required \| default(false) }}"` | Whether the node needs a reboot. Defaults to the fact set by iacker.fleet.apt_upgrade. |
| `k3s_rolling_reboot_force` | bool | `false` | Reboot even if no reboot is required. |
| `k3s_rolling_reboot_drain` | bool | `false` | Drain before rebooting. Off by default, see README. |
| `k3s_rolling_reboot_drain_timeout` | str | `"300s"` | Timeout passed to `kubectl drain`. |
| `k3s_rolling_reboot_timeout` | int | `900` | Maximum time to wait for the node to come back over SSH (seconds). |
| `k3s_rolling_reboot_ready_retries` | int | `30` | Attempts while waiting for the node to be Ready. |
| `k3s_rolling_reboot_ready_delay` | int | `10` | Seconds between Ready checks. |

## Entry point `preflight`

Fail unless every node of the cluster is Ready. Run on the controller.

| Variable | Type | Default | Description |
|---|---|---|---|
| `k3s_rolling_reboot_kubectl` | str | `"kubectl"` | kubectl command on the controller. |

See the [collection README](../../README.md) for complete playbooks.
