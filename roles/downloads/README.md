# marcstraube.desktop.downloads

Install download managers and torrent clients.

## Description

Installs optional download tools: BitTorrent clients (Transmission, qBittorrent,
Deluge), video downloaders (yt-dlp), and download managers (aria2, uGet,
JDownloader). Each application has its own boolean toggle and is independently
installable. Package availability varies by platform — applications not packaged
for a given OS are silently skipped.

## Requirements

- ansible-core >= 2.17
- `kewlfft.aur` collection (Arch Linux AUR packages)
- EPEL repository on Rocky Linux (managed by `marcstraube.common.package_management`)

## Supported Platforms

| Platform                  | Notes                                   |
|---------------------------|-----------------------------------------|
| Arch Linux                | All packages (+ JDownloader via AUR)    |
| Debian Trixie             | All except JDownloader                  |
| EL 9 (Rocky, Alma, RHEL)  | transmission, qbittorrent, aria2 (EPEL) |
| EL 10 (Rocky, Alma, RHEL) | aria2 (EPEL)                            |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable            | Default | Description         |
|---------------------|---------|---------------------|
| `downloads_enabled` | `true`  | Enable/disable role |

### Torrent Clients

| Variable                         | Default | Description          |
|----------------------------------|---------|----------------------|
| `downloads_transmission_enabled` | `true`  | Install Transmission |
| `downloads_qbittorrent_enabled`  | `false` | Install qBittorrent  |
| `downloads_deluge_enabled`       | `false` | Install Deluge       |

### Video Downloaders

| Variable                  | Default | Description    |
|---------------------------|---------|----------------|
| `downloads_ytdlp_enabled` | `false` | Install yt-dlp |

### Download Managers

| Variable                        | Default | Description                     |
|---------------------------------|---------|---------------------------------|
| `downloads_aria2_enabled`       | `false` | Install aria2                   |
| `downloads_uget_enabled`        | `false` | Install uGet                    |
| `downloads_jdownloader_enabled` | `false` | Install JDownloader (Arch only) |

## Tags

| Tag                 | Scope                |
|---------------------|----------------------|
| `downloads`         | All download tasks   |
| `downloads:install` | Package installation |

## Example Playbook

```yaml
- name: Downloads
  hosts: workstations
  tasks:
    - name: Downloads | Include downloads role
      ansible.builtin.include_role:
        name: marcstraube.desktop.downloads
      tags: [downloads]
      when: downloads_enabled | default(true) | bool
```

## Testing

```bash
cd roles/downloads
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
