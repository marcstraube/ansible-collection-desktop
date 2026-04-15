# marcstraube.desktop.imaging

Install imaging and scanning applications.

## Description

Manages installation of scanning backends, scanning frontends, and image
processing tools across Arch Linux, Debian, and EL-based systems. Each
application is individually toggleable via boolean variables. VueScan is
available on Arch Linux only (AUR package).

## Requirements

- ansible-core >= 2.17
- Collections: `kewlfft.aur` (Arch Linux AUR support)

## Supported Platforms

| Platform                   | Notes |
| -------------------------- | ----- |
| Arch Linux                 |       |
| Debian Trixie              |       |
| EL 9 (Rocky, Alma, RHEL)   |       |
| EL 10 (Rocky, Alma, RHEL)  |       |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable          | Default | Description             |
| ----------------- | ------- | ----------------------- |
| `imaging_enabled` | `true`  | Enable the imaging role |

### Scanning Applications

| Variable                      | Default | Description                                                         |
| ----------------------------- | ------- | ------------------------------------------------------------------- |
| `imaging_vuescan_enabled`     | `true`  | Enable VueScan professional scanning software (Arch Linux AUR only) |
| `imaging_sane_enabled`        | `true`  | Enable SANE scanner backend                                         |
| `imaging_xsane_enabled`       | `false` | Enable XSane graphical scanning frontend                            |
| `imaging_simple_scan_enabled` | `false` | Enable Simple Scan (GNOME scanning application)                     |
| `imaging_skanlite_enabled`    | `false` | Enable Skanlite (KDE scanning application)                          |

### Image Processing

| Variable                         | Default | Description                                        |
| -------------------------------- | ------- | -------------------------------------------------- |
| `imaging_imagemagick_enabled`    | `false` | Enable ImageMagick command-line image manipulation |
| `imaging_graphicsmagick_enabled` | `false` | Enable GraphicsMagick image processing system      |

## Tags

| Tag                      | Scope                       |
| ------------------------ | --------------------------- |
| `imaging`                | All role tasks              |
| `imaging:install`        | Package installation        |
| `imaging:vuescan`        | VueScan installation        |
| `imaging:sane`           | SANE installation           |
| `imaging:xsane`          | XSane installation          |
| `imaging:simple-scan`    | Simple Scan installation    |
| `imaging:skanlite`       | Skanlite installation       |
| `imaging:imagemagick`    | ImageMagick installation    |
| `imaging:graphicsmagick` | GraphicsMagick installation |

## Example Playbook

```yaml
- name: Include imaging role
  ansible.builtin.include_role:
    name: marcstraube.desktop.imaging
  tags: [imaging]
  when: imaging_enabled | default(true) | bool
```

## Testing

```bash
cd roles/imaging
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
