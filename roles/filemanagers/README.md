# marcstraube.desktop.filemanagers

Install terminal and GUI file managers.

## Description

Installs optional file managers: terminal-based (vifm, Midnight Commander, ranger,
nnn, lf) and graphical (Thunar, Dolphin, Nautilus, PCManFM, Nemo, Double Commander).
Each application has its own boolean toggle and is independently installable. Package
availability varies by platform -- applications not packaged for a given OS are
silently skipped.

## Requirements

- ansible-core >= 2.17
- EPEL repository on Rocky Linux (managed by `marcstraube.common.package_management`)

## Supported Platforms

| Platform                   | Notes                                     |
| -------------------------- | ----------------------------------------- |
| Arch Linux                 |                                           |
| Debian Trixie              |                                           |
| EL 9 (Rocky, Alma, RHEL)   | lf and Double Commander not available     |
| EL 10 (Rocky, Alma, RHEL)  | lf and Double Commander not available     |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable               | Default | Description         |
| ---------------------- | ------- | ------------------- |
| `filemanagers_enabled` | `true`  | Enable/disable role |

### Terminal File Managers

| Variable                      | Default | Description                           |
| ----------------------------- | ------- | ------------------------------------- |
| `filemanagers_vifm_enabled`   | `false` | Enable vifm (Vi-like file manager)    |
| `filemanagers_mc_enabled`     | `false` | Enable Midnight Commander             |
| `filemanagers_ranger_enabled` | `false` | Enable ranger                         |
| `filemanagers_nnn_enabled`    | `false` | Enable nnn                            |
| `filemanagers_lf_enabled`     | `false` | Enable lf (not available on EL/EPEL)  |

### GUI File Managers

| Variable                         | Default | Description                                        |
| -------------------------------- | ------- | -------------------------------------------------- |
| `filemanagers_thunar_enabled`    | `false` | Enable Thunar (Xfce)                               |
| `filemanagers_dolphin_enabled`   | `false` | Enable Dolphin (KDE)                               |
| `filemanagers_nautilus_enabled`  | `false` | Enable Nautilus (GNOME)                            |
| `filemanagers_pcmanfm_enabled`   | `false` | Enable PCManFM                                     |
| `filemanagers_nemo_enabled`      | `false` | Enable Nemo (Cinnamon)                             |
| `filemanagers_doublecmd_enabled` | `false` | Enable Double Commander (not available on EL/EPEL) |

## Tags

| Tag                    | Scope           |
| ---------------------- | --------------- |
| `filemanagers`         | All tasks       |
| `filemanagers:install` | Package install |

## Example Playbook

```yaml
- name: File managers
  hosts: workstations
  tasks:
    - name: File managers | Include filemanagers role
      ansible.builtin.include_role:
        name: marcstraube.desktop.filemanagers
      tags: [filemanagers]
      when: filemanagers_enabled | default(true) | bool
```

## Testing

```bash
cd roles/filemanagers
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## Notes

- **lf** is not available in EPEL repositories. It is available in official Arch
  Linux repos (extra) and in Debian Trixie.
- **Double Commander** is not available in EPEL repositories. The Arch package is
  `doublecmd-qt5` (GTK2 variant was dropped from official repos). Debian uses
  `doublecmd-gtk`.

## License

MIT

## Author

Marc Straube
