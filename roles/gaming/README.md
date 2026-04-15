# marcstraube.desktop.gaming

Install gaming platforms and emulators.

## Description

Installs Lutris, Steam, RetroArch, PCSX2, Dolphin, Moonlight, Heroic Games
Launcher, and Playback across Arch Linux, Debian Trixie, and Rocky Linux 9/10.
Wine has been extracted into its own role (`marcstraube.desktop.wine`).

Platform availability varies by OS — see the Role Variables table for details.
Tasks with empty package variables are skipped automatically, so the role is safe
to run on all supported platforms without OS-specific conditionals in the inventory.

Arch Linux installs AUR-only packages (Playback, Heroic, PCSX2) via `kewlfft.aur`
using the `aur_builder` user created in the molecule prepare playbook and expected
to exist on managed hosts.

## Requirements

- ansible-core >= 2.17
- `kewlfft.aur` collection (AUR packages on Arch Linux)
- EPEL repository enabled (for Lutris on Rocky Linux 9/10)
- `aur_builder` system user with passwordless sudo (Arch Linux only)

## Supported Platforms

| Platform                   | Notes                                       |
| -------------------------- | ------------------------------------------- |
| Arch Linux                 | Full support — native packages + AUR        |
| Debian Trixie              | Most packages available; Steam removed      |
| EL 9 (Rocky, Alma, RHEL)   | Lutris via EPEL; limited emulators          |
| EL 10 (Rocky, Alma, RHEL)  | Lutris via EPEL; limited emulators          |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable         | Default | Description                |
| ---------------- | ------- | -------------------------- |
| `gaming_enabled` | `true`  | Enable/disable gaming role |

### Gaming Platforms

| Variable                | Default | Arch | Debian | Rocky | Description                                   |
| ----------------------- | ------- | ---- | ------ | ----- | --------------------------------------------- |
| `gaming_lutris_enabled` | `true`  | yes  | yes    | yes   | Lutris gaming platform                        |
| `gaming_steam_enabled`  | `false` | yes  | no*    | no**  | Steam game store                              |
| `gaming_heroic_enabled` | `false` | yes  | no     | no    | Heroic Games Launcher (Epic/GOG) — AUR only   |

\* Steam was removed from Debian testing in January 2023.
\*\* Steam requires RPM Fusion on Rocky Linux (not managed by this role).

### Emulation

| Variable                   | Default | Arch | Debian | Rocky | Description                                |
| -------------------------- | ------- | ---- | ------ | ----- | ------------------------------------------ |
| `gaming_retroarch_enabled` | `true`  | yes  | yes    | no*   | RetroArch emulator frontend                |
| `gaming_playback_enabled`  | `true`  | yes  | no     | no    | Playback game recording viewer — AUR only  |
| `gaming_pcsx2_enabled`     | `false` | yes* | yes    | no**  | PCSX2 PlayStation 2 emulator               |
| `gaming_dolphin_enabled`   | `false` | yes  | yes    | no*   | Dolphin GameCube/Wii emulator              |

\* RetroArch and Dolphin are not available in EPEL 9 or EPEL 10.
\* PCSX2 is installed via AUR on Arch Linux.
\*\* PCSX2 requires RPM Fusion on Rocky Linux (not managed by this role).

### Game Streaming

| Variable                   | Default | Arch | Debian | Rocky | Description                        |
| -------------------------- | ------- | ---- | ------ | ----- | ---------------------------------- |
| `gaming_moonlight_enabled` | `false` | yes  | no     | no    | Moonlight NVIDIA GameStream client |

## Tags

| Tag              | Scope                |
| ---------------- | -------------------- |
| `gaming`         | All gaming tasks     |
| `gaming:install` | Package installation |

## Example Playbook

```yaml
- name: Gaming
  hosts: workstations
  tasks:
    - name: Include gaming role
      ansible.builtin.include_role:
        name: marcstraube.desktop.gaming
      tags: [gaming]
      when: gaming_enabled | default(true) | bool
```

## Testing

```bash
cd roles/gaming
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10
- All installs are disabled in the test converge (non-standard repos required).
  The test confirms the role loads variables and completes without errors on all platforms.

## License

MIT

## Author

Marc Straube
