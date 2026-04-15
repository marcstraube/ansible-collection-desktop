# marcstraube.desktop.communication

Install messaging and communication applications.

## Description

Manages installation of messaging, VoIP, email filtering, and connectivity
applications across Arch Linux, Debian, and EL-based systems. Each application
is individually toggleable via boolean variables. AUR packages are used on
Arch Linux for applications not available in official repositories (Slack,
Threema, Zoom, Teams, Jitsi Meet).

## Requirements

- ansible-core >= 2.17
- Collections: `kewlfft.aur` (Arch Linux AUR support)

## Supported Platforms

| Platform                  | Notes |
|---------------------------|-------|
| Arch Linux                |       |
| Debian Trixie             |       |
| EL 9 (Rocky, Alma, RHEL)  |       |
| EL 10 (Rocky, Alma, RHEL) |       |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                | Default | Description                   |
|-------------------------|---------|-------------------------------|
| `communication_enabled` | `true`  | Enable the communication role |

### Messaging

| Variable                              | Default | Description                       |
|---------------------------------------|---------|-----------------------------------|
| `communication_slack_enabled`         | `true`  | Enable Slack team communication   |
| `communication_slack_wayland_enabled` | `false` | Enable Slack Wayland variant      |
| `communication_telegram_enabled`      | `true`  | Enable Telegram instant messaging |
| `communication_threema_enabled`       | `true`  | Enable Threema secure messaging   |
| `communication_signal_enabled`        | `false` | Enable Signal Desktop             |
| `communication_discord_enabled`       | `false` | Enable Discord                    |
| `communication_element_enabled`       | `false` | Enable Element Matrix client      |

### Email Filters

| Variable                      | Default | Description                                       |
|-------------------------------|---------|---------------------------------------------------|
| `communication_sieve_enabled` | `true`  | Enable Sieve email filtering (ManageSieve client) |

### VoIP

| Variable                      | Default | Description            |
|-------------------------------|---------|------------------------|
| `communication_zoom_enabled`  | `false` | Enable Zoom            |
| `communication_teams_enabled` | `false` | Enable Microsoft Teams |
| `communication_jitsi_enabled` | `false` | Enable Jitsi Meet      |

### Connectivity

| Variable                           | Default | Description                                  |
|------------------------------------|---------|----------------------------------------------|
| `communication_kdeconnect_enabled` | `false` | Enable KDE Connect phone/desktop integration |

## Tags

| Tag                     | Scope                |
|-------------------------|----------------------|
| `communication`         | All role tasks       |
| `communication:install` | Package installation |

## Example Playbook

```yaml
- name: Include communication role
  ansible.builtin.include_role:
    name: marcstraube.desktop.communication
  tags: [communication]
  when: communication_enabled | default(true) | bool
```

## Testing

```bash
cd roles/communication
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
