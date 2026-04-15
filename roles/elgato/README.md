# marcstraube.desktop.elgato

Install and configure tools for Elgato devices.

## Description

Installs optional tools for Elgato hardware on Arch Linux: StreamController for
Stream Deck/Pedal (AUR), cameractrls for Facecam (official repo), and
elgato-keylight for Key Light (AUR). Additionally deploys a WirePlumber config
fix for the Elgato Wave:3 microphone to enable simultaneous playback and
recording.

This role is Arch Linux only. All device tools are AUR or official Arch
packages.

## Requirements

- ansible-core >= 2.17
- `kewlfft.aur` collection (Arch Linux AUR packages)

## Supported Platforms

| Platform   | Notes                       |
| ---------- | --------------------------- |
| Arch Linux | All features (pacman + AUR) |

Other distributions in the Archlinux os_family (EndeavourOS, Manjaro) should
work but are not actively tested.

## Role Variables

### Role Control

| Variable         | Default | Description         |
| ---------------- | ------- | ------------------- |
| `elgato_enabled` | `true`  | Enable/disable role |

### Device Tools

| Variable                    | Default | Description                            |
| --------------------------- | ------- | -------------------------------------- |
| `elgato_streamdeck_enabled` | `false` | Install StreamController (Stream Deck) |
| `elgato_facecam_enabled`    | `false` | Install cameractrls (Facecam)          |
| `elgato_keylight_enabled`   | `false` | Install elgato-keylight (Key Light)    |
| `elgato_wave3_enabled`      | `false` | Deploy Wave:3 WirePlumber config fix   |

### User Configuration

| Variable             | Default | Description                         |
| -------------------- | ------- | ----------------------------------- |
| `elgato_wave3_users` | `[]`    | Users for Wave:3 WirePlumber config |

## Tags

| Tag              | Scope                    |
| ---------------- | ------------------------ |
| `elgato`         | All Elgato tasks         |
| `elgato:install` | Package installation     |
| `elgato:wave3`   | Wave:3 config deployment |

## Example Playbook

```yaml
- name: Elgato
  hosts: workstations
  tasks:
    - name: Elgato | Include elgato role
      ansible.builtin.include_role:
        name: marcstraube.desktop.elgato
      tags: [elgato]
      when: elgato_enabled | default(true) | bool
```

## Testing

```bash
cd roles/elgato
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux

## License

MIT

## Author

Marc Straube
