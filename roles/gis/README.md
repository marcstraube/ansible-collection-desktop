# marcstraube.desktop.gis

Install GIS applications and geospatial tools.

## Description

Installs applications for working with geospatial data. Each application has
its own toggle and is independently installable. Platforms without a package
are a silent no-op; the tables below name the alternative install path.

Supported applications:

- **QGIS**: desktop GIS for viewing, editing and analyzing vector and raster data
- **GDAL**: command-line tools for raster and vector data (`gdalinfo`,
  `ogr2ogr`, `gdal_translate`, `gdalwarp`, …). QGIS pulls in the GDAL
  libraries anyway; the toggle adds the tools, also without QGIS
- **GPlates**: plate tectonic reconstructions and paleogeography

## Requirements

- ansible-core >= 2.19
- EPEL and CRB repositories on EL 9 for QGIS (managed by
  `marcstraube.common.package_management`)
- Arch Linux: an AUR builder account (`aur_builder` by default, set with
  `aur_builder_user`) for GPlates, as set up by
  `marcstraube.common.package_management`

## Supported Platforms

| Platform                  | Notes                                 |
| ------------------------- | ------------------------------------- |
| Arch Linux                | All applications (GPlates from AUR)   |
| Debian Trixie             | QGIS, GDAL                            |
| EL 9 (Rocky, Alma, RHEL)  | QGIS (EPEL + CRB), GDAL (AppStream)   |
| EL 10 (Rocky, Alma, RHEL) | GDAL (AppStream)                      |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable      | Default | Description         |
| ------------- | ------- | ------------------- |
| `gis_enabled` | `false` | Enable/disable role |

### GIS Applications

| Variable              | Default | Description                     |
| --------------------- | ------- | ------------------------------- |
| `gis_qgis_enabled`    | `true`  | Install QGIS                    |
| `gis_gdal_enabled`    | `true`  | Install GDAL command-line tools |
| `gis_gplates_enabled` | `false` | Install GPlates                 |

Availability per platform:

| Application | Arch Linux          | Debian Trixie | EL 9               | EL 10              |
| ----------- | ------------------- | ------------- | ------------------ | ------------------ |
| QGIS        | `qgis` (extra)      | `qgis`        | `qgis` (EPEL)      | Not available      |
| GDAL        | `gdal` (extra)      | `gdal-bin`    | `gdal` (AppStream) | `gdal` (AppStream) |
| GPlates     | `gplates-git` (AUR) | Not available | Not available      | Not available      |

Alternative install paths where the role installs nothing:

- **QGIS on EL 10:** Flathub, `flatpak install flathub org.qgis.qgis`
- **GPlates on Debian and EL:** the source package from
  <https://www.gplates.org/download/> (upstream also ships `.deb` packages
  for supported Ubuntu releases)

GPlates comes from `gplates-git`, which builds the development branch from
source: the release package `gplates` (2.5.0) does not build against GDAL
3.13. The build takes a while and needs Qt 5, Boost and CGAL. The role only
installs the package; `-git` packages update when the AUR helper runs with
`--devel` (e.g. `paru -Syu --devel`).

## Tags

| Tag   | Scope         |
| ----- | ------------- |
| `gis` | All GIS tasks |

## Example Playbook

```yaml
- name: GIS
  hosts: workstations
  tasks:
    - name: GIS | Include gis role
      ansible.builtin.include_role:
        name: marcstraube.desktop.gis
      tags: [gis]
      when: gis_enabled | default(false) | bool
```

Inventory example (`group_vars`/`host_vars`):

```yaml
gis_enabled: true
gis_gplates_enabled: true
```

## Testing

```bash
cd roles/gis
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10
- GPlates is off on Arch Linux in the scenario (no AUR source build in the
  container) and on elsewhere, where the toggle must be a no-op

## References

- [QGIS documentation](https://docs.qgis.org/)
- [GDAL programs](https://gdal.org/en/stable/programs/index.html)
- [GPlates](https://www.gplates.org/)

## License

MIT

## Author

Marc Straube
