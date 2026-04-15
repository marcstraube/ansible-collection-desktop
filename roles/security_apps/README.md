# marcstraube.desktop.security_apps

Install security and encryption applications.

## Description

Installs disk encryption software, hardware wallet clients, a ClamAV GUI,
and a firewall GUI. Application availability varies by platform:

- **VeraCrypt** (disk encryption): Arch Linux only — not packaged for Debian or EPEL.
- **Hardware wallets** (Cypherock CySync, Ledger Live, Trezor Suite): Arch Linux only,
  installed via AUR. Requires the `aur_builder` user and the `kewlfft.aur` collection.
- **ClamTk** (ClamAV GUI): Arch Linux only — removed from Debian Trixie testing
  repositories (April 2026) and not available in EPEL 9 or EPEL 10.
- **Gufw** (firewall GUI): Arch Linux and Debian only — not packaged for Rocky Linux.

## Requirements

- ansible-core >= 2.17
- `community.general` collection
- `kewlfft.aur` collection (hardware wallet AUR packages on Arch Linux only)
- `aur_builder` user with passwordless sudo (Arch Linux, for AUR packages)

## Supported Platforms

| Platform                   | Notes                                         |
|----------------------------|-----------------------------------------------|
| Arch Linux                 | Full support — native packages + AUR          |
| Debian Trixie              | Gufw only; VeraCrypt and ClamTk not available |
| EL 9 (Rocky, Alma, RHEL)   | No packages available in base repos or EPEL   |
| EL 10 (Rocky, Alma, RHEL)  | No packages available in base repos or EPEL   |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                | Default | Description                       |
|-------------------------|---------|-----------------------------------|
| `security_apps_enabled` | `true`  | Enable/disable security_apps role |

### Encryption

| Variable                          | Default | Description                   |
|-----------------------------------|---------|-------------------------------|
| `security_apps_veracrypt_enabled` | `true`  | Install VeraCrypt (Arch only) |

### Hardware Wallets (Arch AUR only)

| Variable                          | Default | Description                    |
|-----------------------------------|---------|--------------------------------|
| `security_apps_cypherock_enabled` | `true`  | Install Cypherock CySync (AUR) |
| `security_apps_ledger_enabled`    | `false` | Install Ledger Live (AUR)      |
| `security_apps_trezor_enabled`    | `false` | Install Trezor Suite (AUR)     |

### Security Tools

| Variable                       | Default | Description                               |
|--------------------------------|---------|-------------------------------------------|
| `security_apps_clamtk_enabled` | `false` | Install ClamTk ClamAV GUI (Arch only)     |
| `security_apps_gufw_enabled`   | `false` | Install Gufw firewall GUI (Arch + Debian) |

## Tags

| Tag                     | Scope                   |
|-------------------------|-------------------------|
| `security-apps`         | All security_apps tasks |
| `security-apps:install` | Package installation    |

## Example Playbook

```yaml
- name: Security apps
  hosts: workstations
  tasks:
    - name: Security apps | Include security_apps role
      ansible.builtin.include_role:
        name: marcstraube.desktop.security_apps
      tags: [security-apps]
      when: security_apps_enabled | default(true) | bool
```

## Testing

```bash
cd roles/security_apps
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
