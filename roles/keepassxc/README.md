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

> **Manual setup required after first run.** Enabling
> `keepassxc_secret_service_enabled` only registers KeePassXC as the
> freedesktop Secret-Service DBus provider. The database group that
> KeePassXC actually exposes to Secret-Service clients must be assigned
> manually **per database** in the KeePassXC GUI — the assignment is
> stored inside the KDBX file and cannot be set by Ansible.
>
> Path in the GUI: `Application Settings → Secret Service Integration →
> Expose entries under this group`. Pick (or create) a group, then save
> the database.
>
> Without this step, every Secret-Service client (Slack, Claude Desktop,
> browsers, …) that contacts KeePassXC triggers a one-time setup wizard
> on first connection that looks like a "create new database" prompt and
> can be confusing.

### SSH Agent Integration

| Variable                      | Default | Description                |
| ----------------------------- | ------- | -------------------------- |
| `keepassxc_ssh_agent_enabled` | `false` | Enable KeePassXC SSH agent |

### Autostart

KeePassXC autostart is managed via the XDG autostart entry
`~/.config/autostart/org.keepassxc.KeePassXC.desktop` — the same file
KeePassXC writes from its GUI checkbox "Automatically launch KeePassXC
at system startup". The role deploys/removes this file based on the
toggle below; KeePassXC and the role share a single source of truth.

| Variable                      | Default         | Description                                        |
| ----------------------------- | --------------- | -------------------------------------------------- |
| `keepassxc_autostart_enabled` | `false`         | Enable KeePassXC autostart via XDG autostart entry |
| `keepassxc_locale`            | `en_US.UTF-8`   | Host-level locale for `GenericName` translation    |

The `GenericName` field in the deployed autostart entry is translated
from the system `.desktop` file (`/usr/share/applications/org.keepassxc.KeePassXC.desktop`)
using the requested locale. Resolution order:

1. Per-user `lang` attribute on the user entry (`keepassxc_users[*].lang`
   or `users_list[*].lang` — both flow through)
2. `keepassxc_locale` (host-level default)
3. English fallback (`GenericName=Password Manager`)

Wire `keepassxc_locale: "{{ base_locale }}"` in inventory to follow a
project-wide locale.

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
    delay: 5                      # Optional, X-GNOME-Autostart-Delay (seconds, default 2)
    lang: 'de_DE.UTF-8'           # Optional, overrides keepassxc_locale for this user
    secret_service: true          # Opt-out with false
    browser_integration: true     # Override global setting
    config:                       # Override specific config values
      Security:
        LockDatabaseIdleSeconds: 600
```

The `mode` key controls per-user config deployment:

- `managed` -- always deploy/overwrite config
- `initial` -- deploy only when `keepassxc.ini` does not yet exist for the user (default)
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

## References

- [KeePassXC](https://keepassxc.org/) — Cross-platform community-driven password manager
- [KeePassXC Documentation](https://keepassxc.org/docs/) — User guide and configuration reference
- [KeePassXC-Browser](https://github.com/keepassxreboot/keepassxc-browser) — Browser extension for autofill
- [Secret Service API](https://specifications.freedesktop.org/secret-service-spec/latest/) — D-Bus API KeePassXC uses

## License

MIT

## Author

Marc Straube
