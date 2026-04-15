# marcstraube.desktop.remote_access

Install remote desktop and access applications.

## Description

Installs remote desktop clients, VNC viewers, RDP clients, and other remote
access tools. Application availability varies by platform:

- **Remmina**, **TigerVNC**, **FreeRDP**: Available on all platforms via official repositories.
- **RustDesk**, **Asbru Connection Manager**, **RealVNC Viewer**, **AnyDesk**, **TeamViewer**:
  Arch Linux only, installed via AUR. Requires the `aur_builder` user and the
  `kewlfft.aur` collection.

## Requirements

- ansible-core >= 2.17
- `community.general` collection
- `kewlfft.aur` collection (AUR packages on Arch Linux only)
- `aur_builder` user with passwordless sudo (Arch Linux, for AUR packages)

## Supported Platforms

| Platform                   | Notes                                    |
| -------------------------- | ---------------------------------------- |
| Arch Linux                 | Full support — native packages + AUR     |
| Debian Trixie              | Official repo packages only              |
| EL 9 (Rocky, Alma, RHEL)   | Official repo packages only              |
| EL 10 (Rocky, Alma, RHEL)  | Official repo packages only              |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                | Default | Description                       |
| ----------------------- | ------- | --------------------------------- |
| `remote_access_enabled` | `true`  | Enable the remote_access role     |

### Remote Desktop

| Variable                         | Default | Description                                      |
|----------------------------------|---------|--------------------------------------------------|
| `remote_access_remmina_enabled`  | `true`  | Enable Remmina remote desktop client             |
| `remote_access_rustdesk_enabled` | `true`  | Enable RustDesk open source remote desktop (AUR) |
| `remote_access_asbru_enabled`    | `true`  | Enable Asbru Connection Manager (AUR)            |

### VNC Clients

| Variable                          | Default | Description                       |
| --------------------------------- | ------- | --------------------------------- |
| `remote_access_tigervnc_enabled`  | `false` | Enable TigerVNC viewer            |
| `remote_access_realvnc_enabled`   | `false` | Enable RealVNC viewer (AUR)       |

### RDP Clients

| Variable                         | Default | Description                                  |
| -------------------------------- | ------- | -------------------------------------------- |
| `remote_access_freerdp_enabled`  | `false` | Enable FreeRDP (often used by Remmina)       |

### Other

| Variable                            | Default | Description                |
| ----------------------------------- | ------- | -------------------------- |
| `remote_access_anydesk_enabled`     | `false` | Enable AnyDesk (AUR)       |
| `remote_access_teamviewer_enabled`  | `false` | Enable TeamViewer (AUR)    |

## Tags

| Tag                      | Scope                |
| ------------------------ | -------------------- |
| `remote-access`          | All role tasks       |
| `remote-access:install`  | Package installation |

## Example Playbook

```yaml
- name: Remote access
  hosts: workstations
  tasks:
    - name: Remote access | Include remote_access role
      ansible.builtin.include_role:
        name: marcstraube.desktop.remote_access
      tags: [remote-access]
      when: remote_access_enabled | default(true) | bool
```

## Testing

```bash
cd roles/remote_access
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
