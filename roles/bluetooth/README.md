# marcstraube.desktop.bluetooth

Install and configure Bluetooth support.

## Description

Installs BlueZ and configures the Bluetooth subsystem. Supports multiple audio
backends (PipeWire, PulseAudio, ALSA), GUI management tools (Blueman, GNOME
Bluetooth, Bluedevil), and OBEX file transfers.

Configures security defaults including MAC address privacy, secure connections,
and pairing timeouts. The ALSA audio backend on Arch Linux is installed via AUR
(`bluez-alsa-git`).

## Requirements

- ansible-core >= 2.17
- `community.general` collection (pacman module)
- `kewlfft.aur` collection (Arch Linux AUR packages)

## Supported Platforms

| Platform                   | Notes                        |
| -------------------------- | ---------------------------- |
| Arch Linux                 | Native packages + AUR (ALSA) |
| Debian Trixie              | Native packages              |
| EL 9 (Rocky, Alma, RHEL)   | Native packages              |
| EL 10 (Rocky, Alma, RHEL)  | Native packages              |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                    | Default | Description                        |
| --------------------------- | ------- | ---------------------------------- |
| `bluetooth_enabled`         | `true`  | Enable/disable role                |
| `bluetooth_service_enabled` | `true`  | Enable and start bluetooth service |

### Packages

| Variable                     | Default      | Description                                      |
| ---------------------------- | ------------ | ------------------------------------------------ |
| `bluetooth_deprecated_tools` | `false`      | Install deprecated tools (hcitool, rfcomm)       |
| `bluetooth_obex`             | `true`       | Install OBEX file transfer support               |
| `bluetooth_audio`            | `'pipewire'` | Audio backend: pipewire, pulseaudio, alsa, none  |
| `bluetooth_gui`              | `'none'`     | GUI tool: blueman, gnome, kde, none              |

### General Settings

| Variable                         | Default  | Description                           |
| -------------------------------- | -------- | ------------------------------------- |
| `bluetooth_auto_enable`          | `true`   | Auto-enable adapter on boot           |
| `bluetooth_discoverable_timeout` | `180`    | Discoverable timeout in seconds       |
| `bluetooth_pairable_timeout`     | `180`    | Pairable timeout in seconds           |
| `bluetooth_always_pairable`      | `false`  | Allow pairing without agent           |
| `bluetooth_device_class`         | `''`     | Device class (empty = default)        |
| `bluetooth_device_name`          | `''`     | Device name (empty = hostname)        |
| `bluetooth_controller_mode`      | `'dual'` | Transport: dual, bredr, le            |
| `bluetooth_name_resolving`       | `true`   | Resolve remote device names           |
| `bluetooth_temporary_timeout`    | `30`     | Temporary device retention in seconds |

### Security

| Variable                         | Default    | Description                               |
| -------------------------------- | ---------- | ----------------------------------------- |
| `bluetooth_privacy`              | `'device'` | Privacy: off, device, network             |
| `bluetooth_secure_connections`   | `'on'`     | Secure Connections: off, on, only         |
| `bluetooth_just_works_repairing` | `'always'` | Just Works policy: always, confirm, never |

### Controller Settings

| Variable                     | Default | Description                   |
| ---------------------------- | ------- | ----------------------------- |
| `bluetooth_fast_connectable` | `false` | Fast connectable (more power) |

### Reconnection

| Variable                        | Default              | Description                           |
| ------------------------------- | -------------------- | ------------------------------------- |
| `bluetooth_reconnect_attempts`  | `7`                  | Link loss reconnect attempts          |
| `bluetooth_reconnect_intervals` | `'1,2,4,8,16,32,64'` | Intervals between attempts in seconds |
| `bluetooth_resume_delay`        | `2`                  | Delay after resume before reconnect   |

### GATT

| Variable                  | Default    | Description                            |
| ------------------------- | ---------- | -------------------------------------- |
| `bluetooth_gatt_cache`    | `'always'` | Cache: always, yes, no                 |
| `bluetooth_gatt_channels` | `3`        | ATT channels (1 disables EATT, max 6)  |

### Advanced

| Variable                        | Default | Description                     |
| ------------------------------- | ------- | ------------------------------- |
| `bluetooth_experimental`        | `false` | D-Bus experimental interfaces   |
| `bluetooth_kernel_experimental` | `false` | Kernel experimental features    |
| `bluetooth_extra_config`        | `{}`    | Extra [General] key=value pairs |

## Tags

| Tag                    | Scope                    |
| ---------------------- | ------------------------ |
| `bluetooth`            | All Bluetooth tasks      |
| `bluetooth:install`    | Package installation     |
| `bluetooth:configure`  | Configuration deployment |
| `bluetooth:service`    | Service management       |

## Example Playbook

```yaml
- name: Bluetooth
  hosts: workstations
  tasks:
    - name: Bluetooth | Include bluetooth role
      ansible.builtin.include_role:
        name: marcstraube.desktop.bluetooth
      tags: [bluetooth]
      when: bluetooth_enabled | default(true) | bool
```

## Testing

```bash
cd roles/bluetooth
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
