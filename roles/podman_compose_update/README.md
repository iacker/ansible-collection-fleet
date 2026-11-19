# iacker.fleet.podman_compose_update

## Entry point `main`

Pull and recreate a podman-compose stack, refusing to fill the disk.

- Checks free space before pulling, backs up files, recreates the stack (through its user systemd unit or podman-compose), waits for the expected containers, prunes replaced images, then runs health and URL checks.

| Variable | Type | Default | Description |
|---|---|---|---|
| `podman_compose_update_project_dir` | path | required | Directory holding the compose file. |
| `podman_compose_update_compose_file` | str | `"compose.yml"` | Compose file name, relative to the project directory. |
| `podman_compose_update_project_name` | str | `""` | Compose project name (`-p`). Empty uses the podman-compose default. |
| `podman_compose_update_systemd_unit` | str | `""` | User systemd unit running the stack. Empty recreates with `up -d --force-recreate`. |
| `podman_compose_update_backup_files` | list | `["{{ podman_compose_update_compose_file }}"]` | Files to back up as `<file>.bak.<timestamp>`. Relative paths start at the project directory. |
| `podman_compose_update_min_free_gb` | int | `8` | Minimum free space (GB) required before pulling. |
| `podman_compose_update_free_space_path` | str | `""` | Path whose filesystem is measured. Empty uses the podman image store (graphRoot). |
| `podman_compose_update_prune_images` | bool | `true` | Prune dangling images before and after the update. |
| `podman_compose_update_journal_vacuum_size` | str | `""` | Cap the systemd journal to this size first (needs become). Empty skips it. |
| `podman_compose_update_pull_timeout` | int | `1800` | Maximum pull time (seconds). |
| `podman_compose_update_expected_containers` | list | `[]` | Container names that must be running and not starting/unhealthy. |
| `podman_compose_update_wait_retries` | int | `30` | Attempts while waiting for containers. |
| `podman_compose_update_wait_delay` | int | `10` | Seconds between attempts. |
| `podman_compose_update_health_commands` | list | `[]` | Commands run on the host after the update, as `name`, `cmd`, `expect` (substring of stdout). |
| `podman_compose_update_url_checks` | list | `[]` | URLs checked from the controller, as `url` and `status` (list of accepted codes). |

See the [collection README](../../README.md) for complete playbooks.
