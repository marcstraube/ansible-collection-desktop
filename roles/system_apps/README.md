# marcstraube.desktop.system_apps

Install desktop system management applications.

## Description

Installs a curated set of system utilities for desktop workstations: disk management
tools (GParted, Filelight, Baobab), hardware management (Solaar for Logitech devices),
system monitors (GNOME System Monitor, Plasma System Monitor), backup tools (Timeshift,
Deja Dup), and GNOME utilities (Seahorse, dconf Editor).

Each application is individually toggled via boolean variables, defaulting to a sensible
baseline (GParted, Filelight, Solaar on by default; optional tools off by default).

On Rocky Linux, EPEL must be enabled before running this role — several packages
(gparted, filelight, solaar, timeshift, deja-dup) are not available in the base repos.

## Requirements

- ansible-core >= 2.17
- `community.general` collection (pacman module on Arch Linux)
- **Rocky Linux:** EPEL repository enabled (via `marcstraube.common.package_management`)

## Supported Platforms

| Platform                   | Notes                                  |
|----------------------------|----------------------------------------|
| Arch Linux                 | Native packages from extra/community   |
| Debian Trixie              | Native packages from main              |
| EL 9 (Rocky, Alma, RHEL)   | EPEL required for most packages        |
| EL 10 (Rocky, Alma, RHEL)  | EPEL required for most packages        |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable              | Default | Description                         |
|-----------------------|---------|-------------------------------------|
| `system_apps_enabled` | `true`  | Enable/disable the system_apps role |

### Disk Management

| Variable                        | Default | Description                         |
|---------------------------------|---------|-------------------------------------|
| `system_apps_gparted_enabled`   | `true`  | Install GParted partition editor    |
| `system_apps_filelight_enabled` | `true`  | Install Filelight disk usage viewer |
| `system_apps_baobab_enabled`    | `false` | Install Baobab GNOME disk analyzer  |

### Hardware Management

| Variable                     | Default | Description                            |
|------------------------------|---------|----------------------------------------|
| `system_apps_solaar_enabled` | `true`  | Install Solaar Logitech device manager |

### System Monitoring

| Variable                                    | Default | Description                   |
|---------------------------------------------|---------|-------------------------------|
| `system_apps_gnome_system_monitor_enabled`  | `false` | Install GNOME System Monitor  |
| `system_apps_plasma_system_monitor_enabled` | `false` | Install Plasma System Monitor |

### Backup and Sync

| Variable                        | Default | Description                          |
|---------------------------------|---------|--------------------------------------|
| `system_apps_timeshift_enabled` | `false` | Install Timeshift system backup tool |
| `system_apps_deja_dup_enabled`  | `false` | Install Deja Dup GNOME backup tool   |

### Utilities

| Variable                           | Default | Description                            |
|------------------------------------|---------|----------------------------------------|
| `system_apps_seahorse_enabled`     | `false` | Install Seahorse GNOME keyring manager |
| `system_apps_dconf_editor_enabled` | `false` | Install dconf Editor                   |

## Tags

| Tag                   | Scope                 |
|-----------------------|-----------------------|
| `system-apps`         | All system_apps tasks |
| `system-apps:install` | Package installation  |

## Example Playbook

```yaml
- name: System apps
  hosts: workstations
  tasks:
    - name: System Apps | Include system_apps role
      ansible.builtin.include_role:
        name: marcstraube.desktop.system_apps
      tags: [system-apps]
      when: system_apps_enabled | default(true) | bool
```

## Testing

```bash
cd roles/system_apps
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
