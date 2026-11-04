# marcstraube.desktop.printing_3d

Install slicers and tools for FDM and resin (MSLA) 3D printers.

## Description

Installs slicers that prepare a finished model for a specific printer. Each
application has its own toggle and is independently installable. Platforms
without a package are a silent no-op; the tables below name the alternative
install path. Modeling applications live in the `cad` role.

Applications that need environment variables to work around GPU or toolkit
issues get them through a desktop entry override, scoped to that application
(see [Application Environment](#application-environment)).

## Requirements

- ansible-core >= 2.19
- Arch Linux: an AUR builder account (`aur_builder` by default, set with
  `aur_builder_user`) for the AUR packages, as set up by
  `marcstraube.common.package_management`
- `marcstraube.desktop.desktop_entries` (same collection) writes the desktop
  entry overrides and the UVtools entry; the role includes it, no setup needed

## Supported Platforms

| Platform                  | Notes                                              |
| ------------------------- | -------------------------------------------------- |
| Arch Linux                | All applications (PrusaSlicer from extra, AUR)     |
| Debian Trixie             | PrusaSlicer, UltiMaker Cura                        |
| EL 9 (Rocky, Alma, RHEL)  | No packages; use Flathub, AppImage or vendor files |
| EL 10 (Rocky, Alma, RHEL) | No packages; use Flathub, AppImage or vendor files |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable              | Default | Description         |
| --------------------- | ------- | ------------------- |
| `printing_3d_enabled` | `false` | Enable/disable role |

### FDM Slicers

| Variable                          | Default | Description                           |
| --------------------------------- | ------- | ------------------------------------- |
| `printing_3d_orcaslicer_enabled`  | `false` | Install OrcaSlicer (Arch only)        |
| `printing_3d_prusaslicer_enabled` | `false` | Install PrusaSlicer (Arch, Debian)    |
| `printing_3d_cura_enabled`        | `false` | Install UltiMaker Cura (Arch, Debian) |

### Resin (MSLA) Slicers and Tools

| Variable                       | Default | Description                        |
| ------------------------------ | ------- | ---------------------------------- |
| `printing_3d_chitubox_enabled` | `false` | Install Chitubox Basic (Arch only) |
| `printing_3d_lychee_enabled`   | `false` | Install Lychee Slicer (Arch only)  |
| `printing_3d_uvtools_enabled`  | `false` | Install UVtools (Arch only)        |

### Availability

| Application    | Arch Linux              | Debian 13      | EL 9 / EL 10 |
| -------------- | ----------------------- | -------------- | ------------ |
| OrcaSlicer     | AUR `orca-slicer-bin`   | no-op          | no-op        |
| PrusaSlicer    | `prusa-slicer` (extra)  | `prusa-slicer` | no-op        |
| UltiMaker Cura | AUR `cura-bin`          | `cura`         | no-op        |
| Chitubox Basic | AUR `chitubox-free-bin` | no-op          | no-op        |
| Lychee Slicer  | AUR `lycheeslicer`      | no-op          | no-op        |
| UVtools        | AUR `uvtools-bin`       | no-op          | no-op        |

Alternative install paths where the role installs nothing:

- **OrcaSlicer**: Flathub `com.orcaslicer.OrcaSlicer`
- **PrusaSlicer**: Flathub `com.prusa3d.PrusaSlicer`
- **UltiMaker Cura**: Flathub `com.ultimaker.cura`, or the AppImage from
  <https://ultimaker.com/software/ultimaker-cura/>
- **Chitubox Basic**: the Linux installer from <https://www.chitubox.com/en/download/chitubox-free>
- **Lychee Slicer**: the AppImage from <https://mango3d.io/downloads>
- **UVtools**: the AppImage from <https://github.com/sn4k3/UVtools/releases>

Debian 13 ships Cura 5.0. For a current release, use the AppImage instead of
`printing_3d_cura_enabled`.

### Application Environment

| Variable                  | Default | Description                                     |
| ------------------------- | ------- | ----------------------------------------------- |
| `printing_3d_environment` | `{}`    | Environment variables per application (mapping) |

The keys are the application names of the toggles: `orcaslicer`,
`prusaslicer`, `cura`, `chitubox`, `lychee` and `uvtools`. Each value is a
mapping of environment variables. For every entry except `uvtools` the role
creates overrides through `marcstraube.desktop.desktop_entries`: it copies
the packaged desktop entries of the application from
`/usr/share/applications/` to `/usr/local/share/applications/`, which takes
precedence, and prefixes every `Exec=` line (including the ones of
`[Desktop Action]` groups) with `env NAME=value …`, sorted by name:

| Application | Desktop entries                                   |
| ----------- | ------------------------------------------------- |
| orcaslicer  | `orca-slicer.desktop`                             |
| prusaslicer | `PrusaSlicer.desktop`, `PrusaGcodeviewer.desktop` |
| cura        | `com.ultimaker.cura.desktop`                      |
| chitubox    | `chitubox-basic.desktop`                          |
| lychee      | `lycheeslicer.desktop`                            |

- An application that is not installed (no packaged entry) gets no
  override; an override deployed earlier is removed.
- `uvtools` sets the `Exec=` line of the role-provided UVtools entry instead
  (see [UVtools Desktop Entry](#uvtools-desktop-entry)).
- Every file starts with the marker line
  `# Managed by Ansible (marcstraube.desktop.printing_3d)`, followed by the
  `ansible_managed` header. Removing an entry from the mapping removes its
  overrides; only files with this marker are removed, so a desktop entry
  placed there by hand stays.
- An existing file of the same name without this marker (placed by hand or
  by another role) blocks the override: the run fails with a message naming
  the file. Remove or rename it by hand.
- Variable names consist of letters, digits and underscores; values of
  letters, digits and `_ . , : / = + @ -`. Other values fail the run, since
  they would need quoting in the `Exec=` key. Unknown application names fail
  as well.
- An updated package that changes its desktop entry is picked up on the next
  run.
- Session-wide mechanisms (`environment.d`, `/etc/environment`, profile
  scripts) are not used: these workarounds would change every OpenGL and
  WebKitGTK application of the session.
- Applications started from a terminal or a Flatpak do not read the override.

Example: OrcaSlicer crashes when slicing on some GPU and driver
combinations. Disabling the WebKitGTK DMA-BUF renderer and running OpenGL
through Mesa Zink (on top of Vulkan) avoids the crash:

```yaml
printing_3d_environment:
  orcaslicer:
    WEBKIT_DISABLE_DMABUF_RENDERER: '1'
    MESA_LOADER_DRIVER_OVERRIDE: 'zink'
```

The override then starts OrcaSlicer with:

```ini
Exec=env MESA_LOADER_DRIVER_OVERRIDE=zink WEBKIT_DISABLE_DMABUF_RENDERER=1 /opt/orca-slicer/AppRun %U
```

### UVtools Desktop Entry

`uvtools-bin` ships the AppImage and the `/usr/bin/uvtools` link, but no
desktop entry and no icon, so UVtools would not show up in application
launchers. While `printing_3d_uvtools_enabled` is on and `/usr/bin/uvtools`
exists, the role deploys `/usr/local/share/applications/uvtools.desktop`
through `marcstraube.desktop.desktop_entries`:

- `Exec=uvtools %F`, prefixed with `env NAME=value …` (sorted by name) when
  `printing_3d_environment.uvtools` is set; the same rules for names and
  values apply as for the overrides.
- `Icon=applications-engineering`, a generic icon from the icon theme, since
  the package ships none.
- No `MimeType=`: the resin printer formats UVtools opens (`.ctb`, `.sl1`,
  `.pwmx`, …) have no registered MIME types.
- Without `/usr/bin/uvtools` (Debian, EL, or before the package is
  installed) nothing is deployed.
- Turning `printing_3d_uvtools_enabled` off removes the entry if it carries
  the role's marker line; the package stays installed.
- As with the overrides, a hand-made `uvtools.desktop` without the marker
  blocks the entry with an error instead of being overwritten.

```yaml
printing_3d_uvtools_enabled: true
printing_3d_environment:
  uvtools:
    DOTNET_SYSTEM_GLOBALIZATION_INVARIANT: '1'
```

## Tags

| Tag           | Scope                 |
| ------------- | --------------------- |
| `printing-3d` | All printing_3d tasks |

## Example Playbook

```yaml
- name: 3D printing
  hosts: workstations
  tasks:
    - name: 3D printing | Include printing_3d role
      ansible.builtin.include_role:
        name: marcstraube.desktop.printing_3d
      tags: [printing-3d]
      when: printing_3d_enabled | default(false) | bool
```

```yaml
# host_vars/<host>/vars.yml
printing_3d_enabled: true
printing_3d_orcaslicer_enabled: true
printing_3d_prusaslicer_enabled: true
printing_3d_lychee_enabled: true
```

## Testing

```bash
cd roles/printing_3d
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10
- PrusaSlicer (Arch Linux, Debian) and Cura (Debian) install from the
  distribution; the AUR-only toggles are enabled on Debian and EL, where they
  are a no-op. AUR builds do not run in the containers.
- The environment override runs against a fixture entry for OrcaSlicer on
  Arch Linux and the packaged Cura entry on Debian, followed by a run with an
  empty mapping that removes the overrides and keeps a foreign entry.
- A foreign `lycheeslicer.desktop` (no marker) next to a fixture packaged
  entry on Arch Linux survives the removal run, and a Lychee environment
  that would overwrite it fails with the refusal of the helper.
- UVtools on Arch Linux: a local stub package named `uvtools-bin` provides
  `/usr/bin/uvtools`, so the AUR task finds the package installed and builds
  nothing. The role-provided entry is checked with and without an
  environment and removed when the toggle is off.

## Notes

### Serial Devices

Printing over USB from the slicer and firmware updates of the printer
board need access to the serial device (`/dev/ttyUSB*`, `/dev/ttyACM*`),
which belongs to the serial device group: `uucp` on Arch Linux,
`dialout` on Debian and EL. The group is a general group and is added
through `marcstraube.common.users`, not by this role:

```yaml
users_list:
  - name: 'johndoe'
    groups: ['uucp']      # Arch Linux; 'dialout' on Debian and EL
```

The membership takes effect at the next login.

## References

- [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)
- [PrusaSlicer](https://github.com/prusa3d/PrusaSlicer)
- [UltiMaker Cura](https://github.com/Ultimaker/Cura)
- [Chitubox](https://www.chitubox.com/)
- [Lychee Slicer](https://mango3d.io/)
- [UVtools](https://github.com/sn4k3/UVtools)
- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/)

## License

MIT

## Author

Marc Straube
