# marcstraube.desktop.tuxedo

Install Tuxedo kernel drivers and control center.

## Description

Installs TUXEDO Computers hardware support on Arch Linux: kernel drivers (DKMS)
for keyboard backlight, fan control and Fn keys, the Tuxedo Control Center
daemon for power profiles and fan curves, and an optional YT6801 Ethernet driver
for Gen9/Gen10 models.

The role validates that it runs on Arch Linux and warns about auto-cpufreq
conflicts with the tccd power management daemon.

## Requirements

- ansible-core >= 2.17
- `kewlfft.aur` collection (Arch Linux AUR packages)
- TUXEDO hardware (validated at runtime, non-fatal warning)

## Supported Platforms

| Platform   | Notes                     |
| ---------- | ------------------------- |
| Arch Linux | All features (AUR + DKMS) |

Other distributions in the same os_family (EndeavourOS, Manjaro) should work
but are not actively tested. Use distro-specific vars overrides if needed.

## Role Variables

### Role Control

| Variable         | Default | Description         |
| ---------------- | ------- | ------------------- |
| `tuxedo_enabled` | `true`  | Enable/disable role |

### Packages

| Variable                         | Default | Description                              |
| -------------------------------- | ------- | ---------------------------------------- |
| `tuxedo_drivers_enabled`         | `true`  | Install tuxedo-drivers-dkms              |
| `tuxedo_control_center_enabled`  | `true`  | Install tuxedo-control-center-bin        |
| `tuxedo_yt6801_ethernet_enabled` | `false` | Install YT6801 Ethernet driver (Gen9/10) |

### Services

| Variable                    | Default | Description               |
| --------------------------- | ------- | ------------------------- |
| `tuxedo_tccd_enabled`       | `true`  | Enable tccd service       |
| `tuxedo_tccd_sleep_enabled` | `true`  | Enable tccd-sleep service |

### Warnings

| Variable                        | Default | Description                     |
| ------------------------------- | ------- | ------------------------------- |
| `tuxedo_warn_conflicts_enabled` | `true`  | Check for auto-cpufreq conflict |

## Tags

| Tag               | Scope                |
| ----------------- | -------------------- |
| `tuxedo`          | All Tuxedo tasks     |
| `tuxedo:validate` | Platform validation  |
| `tuxedo:install`  | Package installation |
| `tuxedo:service`  | Service management   |

## Example Playbook

```yaml
- name: Tuxedo
  hosts: workstations
  tasks:
    - name: Tuxedo | Include tuxedo role
      ansible.builtin.include_role:
        name: marcstraube.desktop.tuxedo
      tags: [tuxedo]
      when: tuxedo_enabled | default(true) | bool
```

## Testing

```bash
cd roles/tuxedo
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux
- **Note:** Hardware-dependent features (DKMS, AUR builds, services) are
  disabled in molecule tests. The test validates role syntax, variable loading,
  and platform assertion only.

## License

MIT

## Author

Marc Straube
