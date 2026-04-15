# marcstraube.desktop.cad

Install CAD and 3D modeling applications.

## Description

Installs optional CAD and 3D modeling applications. Each application has its own
boolean toggle and is independently installable. Package availability varies by
platform — applications not packaged for a given OS are silently skipped.

Supported applications: OpenSCAD, FreeCAD, LibreCAD, QCAD, Blender, KiCad.

## Requirements

- ansible-core >= 2.17
- EPEL repository on Rocky Linux (managed by `marcstraube.common.package_management`)

## Supported Platforms

| Platform                   | Notes                          |
| -------------------------- | ------------------------------ |
| Arch Linux                 | All packages available         |
| Debian Trixie              | All except QCAD                |
| EL 9 (Rocky, Alma, RHEL)   | openscad, blender (EPEL + CRB) |
| EL 10 (Rocky, Alma, RHEL)  | openscad (EPEL)                |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable      | Default | Description         |
| ------------- | ------- | ------------------- |
| `cad_enabled` | `true`  | Enable/disable role |

### Applications

| Variable               | Default | Description                     |
| ---------------------- | ------- | ------------------------------- |
| `cad_openscad_enabled` | `true`  | Install OpenSCAD (3D modeler)   |
| `cad_freecad_enabled`  | `false` | Install FreeCAD (3D CAD)        |
| `cad_librecad_enabled` | `false` | Install LibreCAD (2D CAD)       |
| `cad_qcad_enabled`     | `false` | Install QCAD (2D CAD)           |
| `cad_blender_enabled`  | `false` | Install Blender (3D suite)      |
| `cad_kicad_enabled`    | `false` | Install KiCad (electronics EDA) |

## Tags

| Tag   | Scope         |
| ----- | ------------- |
| `cad` | All CAD tasks |

## Example Playbook

```yaml
- name: CAD
  hosts: workstations
  tasks:
    - name: CAD | Include cad role
      ansible.builtin.include_role:
        name: marcstraube.desktop.cad
      tags: [cad]
      when: cad_enabled | default(true) | bool
```

## Testing

```bash
cd roles/cad
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
