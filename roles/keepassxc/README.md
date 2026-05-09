# keepassxc

Install and configure KeePassXC password manager with browser integration,
Secret Service (freedesktop.org) support, SSH agent integration, and
per-user configuration management.

## Requirements

- `community.general` collection (for `ini_file` module)

Browser extension installation is handled by the `marcstraube.desktop.browser`
role via policies.json. This role only manages KeePassXC application settings.

## Supported Platforms

| Platform                   | Notes |
| -------------------------- | ----- |
| Arch Linux                 |       |
| Debian Trixie              |       |
| EL 9 (Rocky, Alma, RHEL)   |       |
| EL 10 (Rocky, Alma, RHEL)  |       |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable            | Default | Description               |
| ------------------- | ------- | ------------------------- |
| `keepassxc_enabled` | `true`  | Enable the keepassxc role |

### Installation

| Variable                            | Default | Description               |
| ----------------------------------- | ------- | ------------------------- |
| `keepassxc_install_package_enabled` | `true`  | Install keepassxc package |

### Browser Integration

| Variable                                  | Default | Description                                      |
| ----------------------------------------- | ------- | ------------------------------------------------ |
| `keepassxc_browser_integration_enabled`   | `true`  | Enable browser integration in KeePassXC settings |

### Secret Service Integration

| Variable                             | Default | Description                                         |
| ------------------------------------ | ------- | --------------------------------------------------- |
| `keepassxc_secret_service_enabled`   | `false` | Enable Secret Service (freedesktop.org) integration |
| `keepassxc_secret_service_scope`     | `'user'`| Secret Service scope: `'user'` or `'global'`        |

### SSH Agent Integration

| Variable                      | Default | Description                |
| ----------------------------- | ------- | -------------------------- |
| `keepassxc_ssh_agent_enabled` | `false` | Enable KeePassXC SSH agent |

### Systemd Autostart

| Variable                      | Default | Description                                         |
| ----------------------------- | ------- | --------------------------------------------------- |
| `keepassxc_autostart_enabled` | `false` | Enable KeePassXC autostart via systemd user service |

### Configuration

| Variable                          | Default             | Description                                                |
| --------------------------------- | ------------------- | ---------------------------------------------------------- |
| `keepassxc_deploy_config_enabled` | `false`             | Deploy default configuration file                          |
| `keepassxc_user_config_mode`      | `initial`           | Default config mode: `managed`, `initial`, or `disabled`   |
| `keepassxc_config_dir`            | `.config/keepassxc` | Configuration directory (relative to home)                 |
| `keepassxc_config`                | *(see defaults)*    | Configuration settings dict                                |

### Users

| Variable          | Default | Description                           |
| ----------------- | ------- | ------------------------------------- |
| `keepassxc_users` | `[]`    | Users list for per-user configuration |

User config mode semantics:

| Mode      | First run | Subsequent runs                          |
|-----------|-----------|------------------------------------------|
| `managed` | deploy    | overwrite (always reconcile to template) |
| `initial` | deploy    | leave existing user customisations alone |
| `disabled`| skip      | skip                                     |

`'initial'` is the default: deploys when `~/.config/keepassxc/keepassxc.ini`
is absent for the user, otherwise leaves the file untouched. Per-user
override via `item.mode` takes precedence over the role-level default.

Each user entry supports:

```yaml
keepassxc_users:
  - name: 'johndoe'
    group: 'johndoe'              # Optional, defaults to name
    mode: 'managed'               # managed/initial/disabled
    autostart: true               # Opt-out with false
    secret_service: true          # Opt-out with false
    browser_integration: true     # Override global setting
    config:                       # Override specific config values
      Security:
        LockDatabaseIdleSeconds: 600
```

The `mode` key controls per-user config deployment:

- `managed` -- always deploy/overwrite config (default)
- `initial` -- deploy only when user is newly created
- `disabled` -- skip config deployment for this user

## Tags

- `keepassxc`

## Example Playbook

```yaml
- hosts: workstations
  become: true

  tasks:
    - name: Include keepassxc role
      ansible.builtin.include_role:
        name: marcstraube.desktop.keepassxc
      tags:
        - keepassxc
```

## Testing

```bash
cd collections/ansible_collections/marcstraube/desktop
molecule test -s default -- --tags keepassxc
```

## License

MIT

## Author

Marc Straube
