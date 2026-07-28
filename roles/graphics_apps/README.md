# marcstraube.desktop.graphics_apps

Install graphics and image editing applications.

## Description

Installs graphics, digital painting, vector graphics, and image conversion
applications. Supports GIMP, Krita, Inkscape, XnConvert, and XnView.

XnConvert and XnView are Arch Linux-only (installed from AUR). On EL, GIMP and
Inkscape come from AppStream on EL 9 but are not packaged for EL 10. Krita is
the opposite: absent on EL 9 (not in EPEL 9), available on EL 10 via EPEL 10.

Optional GIMP plugins can be installed via `graphics_apps_gimp_plugins`, and
Inkscape extensions via `graphics_apps_inkscape_plugins`. On Arch the latter are
installed from the AUR (e.g. `inkscape-silhouette-git`); on Debian/EL they must be
available as distribution packages.

## Requirements

- ansible-core >= 2.17
- `community.general` collection (pacman module)
- `kewlfft.aur` collection (Arch Linux AUR packages)
- On EL 10, Krita requires EPEL and CRB enabled (its turbojpeg dependency lives
  in CRB); GIMP and Inkscape are not packaged for EL 10, and on EL 9 both come
  from AppStream. EPEL and CRB are managed by the
  `marcstraube.common.package_management` role.

## Supported Platforms

| Platform                   | GIMP | Krita   | Inkscape | XnConvert | XnView |
| -------------------------- | ---- | ------- | -------- | --------- | ------ |
| Arch Linux                 | yes  | yes     | yes      | AUR       | AUR    |
| Debian Trixie              | yes  | yes     | yes      | no        | no     |
| EL 9 (Rocky, Alma, RHEL)   | yes  | no      | yes      | no        | no     |
| EL 10 (Rocky, Alma, RHEL)  | no   | EPEL 10 | no       | no        | no     |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                | Default | Description         |
| ----------------------- | ------- | ------------------- |
| `graphics_apps_enabled` | `true`  | Enable/disable role |

### Applications to Install

| Variable                          | Default | Description                                |
| --------------------------------- | ------- | ------------------------------------------ |
| `graphics_apps_gimp_enabled`      | `true`  | Install GIMP                               |
| `graphics_apps_krita_enabled`     | `true`  | Install Krita (skipped on EL 9)            |
| `graphics_apps_inkscape_enabled`  | `true`  | Install Inkscape                           |
| `graphics_apps_xnconvert_enabled` | `true`  | Install XnConvert (Arch only, AUR)         |
| `graphics_apps_xnview_enabled`    | `false` | Install XnView (Arch only, AUR)            |
| `graphics_apps_gimp_plugins`      | `[]`    | Additional GIMP plugin packages to install |
| `graphics_apps_inkscape_plugins`  | `[]`    | Additional Inkscape extension packages     |

## Tags

| Tag             | Scope                   |
| --------------- | ----------------------- |
| `graphics-apps` | All graphics_apps tasks |

## Example Playbook

```yaml
- name: Graphics Apps
  hosts: workstations
  tasks:
    - name: Main | Include graphics_apps role
      ansible.builtin.include_role:
        name: marcstraube.desktop.graphics_apps
      tags: [graphics-apps]
      when: graphics_apps_enabled | bool
```

## Testing

```bash
cd roles/graphics_apps
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
