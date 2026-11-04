# marcstraube.desktop.desktop_entries

Override packaged desktop entries and provide desktop entries for
applications whose package ships none.

Several roles need to change how a desktop application starts or shows up:
environment variables that work around a driver or toolkit issue on a host,
a different name or icon, extra categories, or a launcher for an
application without one. Other roles include one of the entry points of
this role with `include_role` and `tasks_from` instead of each implementing
the copy, the edits, the marker and the removal. The role has no standalone
run.

Entry points:

| Entry point    | Description                                                                |
|----------------|----------------------------------------------------------------------------|
| `override.yml` | Copy of a packaged entry with environment, `set` and `append` changes      |
| `entry.yml`    | Role-provided entry from fields, for applications whose package ships none |

Both write to `/usr/local/share/applications/`. That directory comes before
`/usr/share/applications/` in the default `XDG_DATA_DIRS`
(`/usr/local/share:/usr/share`), so an entry there takes precedence over the
packaged entry of the same name. The packaged entry stays untouched, and
package updates never overwrite the override.

## Requirements

- ansible-core >= 2.19

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

The role has no `desktop_entries_enabled` toggle and no inventory
variables: it never runs on its own, and the calling roles keep their own
toggles and variables (for example `<role>_environment`, see
[Application Environment](#application-environment)).

### Caller Variables

The calling role passes the values as `vars` of the `include_role` task.
They describe one desktop entry and have no role defaults; optional
variables fall back to the value in the table.

Both entry points:

| Variable                      | Required | Default | Description                                          |
|-------------------------------|----------|---------|------------------------------------------------------|
| `desktop_entries_caller`      | yes      |         | Calling role, e.g. `printing_3d`; part of the marker |
| `desktop_entries_file`        | yes      |         | File name of the entry, e.g. `orca-slicer.desktop`   |
| `desktop_entries_environment` | no       | `{}`    | Environment variables for every `Exec=` line         |

`override.yml`:

| Variable                 | Required | Default | Description                                                    |
|--------------------------|----------|---------|----------------------------------------------------------------|
| `desktop_entries_set`    | no       | `{}`    | Keys of `[Desktop Entry]` to replace or add (key: value)       |
| `desktop_entries_append` | no       | `{}`    | List keys of `[Desktop Entry]` to extend (key: list of values) |

`entry.yml`:

| Variable                       | Required       | Default     | Description                                    |
|--------------------------------|----------------|-------------|------------------------------------------------|
| `desktop_entries_state`        | no             | `'present'` | `present` writes, `absent` removes the entry   |
| `desktop_entries_name`         | with `present` |             | `Name=`                                        |
| `desktop_entries_exec`         | with `present` |             | `Exec=`, with field codes such as `%F`         |
| `desktop_entries_generic_name` | no             | `''`        | `GenericName=`; empty: key left out            |
| `desktop_entries_comment`      | no             | `''`        | `Comment=`; empty: key left out                |
| `desktop_entries_icon`         | no             | `''`        | `Icon=` (name or path); empty: key left out    |
| `desktop_entries_categories`   | no             | `[]`        | `Categories=`                                  |
| `desktop_entries_mime_types`   | no             | `[]`        | `MimeType=`                                    |
| `desktop_entries_terminal`     | no             | `false`     | `Terminal=` (boolean)                          |

`desktop_entries_caller` is the role name without the collection, in
lowercase letters, digits and underscores. `desktop_entries_file` is a
desktop file ID: a file name ending in `.desktop`, without a directory.

### Behavior of override.yml

With at least one of `desktop_entries_environment`, `desktop_entries_set` and
`desktop_entries_append` set, the role reads
`/usr/share/applications/<file>` and writes
`/usr/local/share/applications/<file>`: the marker line, the
`ansible_managed` header and the packaged content with the changes:

- `desktop_entries_environment`: every `Exec=` line, the ones of
  `[Desktop Action …]` groups included, gets the prefix `env NAME=value …`
  with the variables sorted by name. A launcher action then starts the
  application with the same environment. A packaged `Exec=` that already
  starts with `env` gets the prefix too (`env A=1 env B=2 app` works)
- `desktop_entries_set`: in the `[Desktop Entry]` group, an existing key is
  replaced and a missing key is added at the end of the group. Only the
  exact key matches: `Name` replaces `Name=`, never the localized
  `Name[de]=`. Booleans are written as `true`/`false`
- `desktop_entries_append`: list keys of the `[Desktop Entry]` group
  (`Categories`, `Keywords`, `MimeType`, …). Values not yet in the list are
  appended in the given order, values already present are skipped, a missing
  key is created; the list ends with `;`. Applied after `desktop_entries_set`

Everything else (comments, other keys, other groups, localized keys) stays as
the package ships it. The override follows the packaged entry: a package
update that changes the entry changes the override on the next run.

Without any change, or when the packaged entry is missing (the application
is not installed, or its package ships no entry of that name), the role
removes the override of this caller and writes nothing. The call does not
fail.

### Behavior of entry.yml

With `desktop_entries_state: present` the role writes
`/usr/local/share/applications/<file>` with the marker line, the
`ansible_managed` header, `Type=Application` and the fields. The environment
prefixes the `Exec=` line in the same form as with `override.yml`.

With `desktop_entries_state: absent` the role removes the entry of this
caller. The calling role passes `absent` when its toggle for the application
is off, so the launcher disappears with the feature; the package stays
installed.

### Marker

The first line of every file the role writes names the calling role:

```text
# Managed by Ansible (marcstraube.desktop.printing_3d)
```

A removal only deletes a file that carries the marker of the same caller. An
entry placed in `/usr/local/share/applications/` by hand, by another role or
by another caller of this role stays.

Writing never replaces such a file either. Before `override.yml` or
`entry.yml` writes, the role checks an existing file at the target path:
with the marker of the same caller it is updated, otherwise (no marker, or
the marker of another caller) the call fails with a message that names the
caller and the file. Remove or rename the file by hand, or choose another
`desktop_entries_file`.

### Validation

Every call validates its values before any change and fails with a message
that names the caller, the file and the invalid names or keys:

| Value                                    | Allowed                                 |
|------------------------------------------|-----------------------------------------|
| Environment variable names               | `[A-Za-z_][A-Za-z0-9_]*`                |
| Environment values                       | Letters, digits and `_ . , : / = + @ -` |
| `set` and `append` keys                  | `[A-Za-z0-9-]+` (no locale suffix)      |
| `set` values and `entry.yml` text fields | No line breaks                          |
| `append` values, categories, MIME types  | No line breaks and no `;`               |

## Tags

The role defines no tags of its own. The `include_role` task of the calling
role carries the tags; use `apply` to pass them on to the included tasks:

```yaml
- name: Environment | Override the OrcaSlicer desktop entry
  ansible.builtin.include_role:
    name: marcstraube.desktop.desktop_entries
    tasks_from: override.yml
    apply:
      tags:
        - printing-3d
  vars:
    desktop_entries_caller: 'printing_3d'
    desktop_entries_file: 'orca-slicer.desktop'
    desktop_entries_environment: "{{ printing_3d_environment['orcaslicer'] | default({}) }}"
  tags:
    - printing-3d
```

## Example Playbook

The role is meant for other roles. A calling role passes the values of its
own variables; an empty environment removes the override again.

Environment workaround for OrcaSlicer (WebKitGTK renderer and Mesa driver on
a host where the default crashes):

```yaml
- name: Environment | Override the OrcaSlicer desktop entry
  ansible.builtin.include_role:
    name: marcstraube.desktop.desktop_entries
    tasks_from: override.yml
  vars:
    desktop_entries_caller: 'printing_3d'
    desktop_entries_file: 'orca-slicer.desktop'
    desktop_entries_environment: "{{ printing_3d_environment['orcaslicer'] | default({}) }}"
```

With `printing_3d_environment` in the inventory of that host:

```yaml
printing_3d_environment:
  orcaslicer:
    WEBKIT_DISABLE_DMABUF_RENDERER: '1'
    MESA_LOADER_DRIVER_OVERRIDE: 'zink'
```

Another name, a window class and extra categories:

```yaml
- name: Configure | Adjust the packaged desktop entry
  ansible.builtin.include_role:
    name: marcstraube.desktop.desktop_entries
    tasks_from: override.yml
  vars:
    desktop_entries_caller: 'example_role'
    desktop_entries_file: 'org.example.App.desktop'
    desktop_entries_set:
      Name: 'Example'
      StartupWMClass: 'example'
    desktop_entries_append:
      Categories:
        - 'Development'
      Keywords:
        - 'editor'
```

Role-provided launcher for an application whose package ships none, present
while the toggle of the calling role is on:

```yaml
- name: Desktop Entry | Manage the UVtools entry
  ansible.builtin.include_role:
    name: marcstraube.desktop.desktop_entries
    tasks_from: entry.yml
  vars:
    desktop_entries_caller: 'printing_3d'
    desktop_entries_file: 'uvtools.desktop'
    desktop_entries_state: "{{ printing_3d_uvtools_enabled | bool | ternary('present', 'absent') }}"
    desktop_entries_name: 'UVtools'
    desktop_entries_generic_name: 'MSLA/DLP slicer file viewer and editor'
    desktop_entries_comment: 'Inspect, repair, convert and edit resin printer files'
    desktop_entries_exec: 'uvtools %F'
    desktop_entries_icon: 'applications-engineering'
    desktop_entries_categories:
      - 'Graphics'
      - '3DGraphics'
      - 'Engineering'
    desktop_entries_environment: "{{ printing_3d_environment['uvtools'] | default({}) }}"
```

## Testing

```bash
cd roles/desktop_entries
molecule test
```

Driver: Podman. Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10.

`prepare.yml` places fixture packaged entries in
`/usr/share/applications/` (one with a `[Desktop Action]` group, a localized
`Name[de]=` and a `Categories=` list) and an entry without a marker in
`/usr/local/share/applications/`. `converge.yml` calls the entry points
directly with fixture values; `verify.yml` checks:

- the `env` prefix on both `Exec=` lines of the override
- `set` replaces `Name=` but not `Name[de]=` or the `Name=` of the action
  group, and adds a new key at the end of `[Desktop Entry]`
- `append` adds a category once (values already present or listed twice are
  skipped, also on the second converge run) and creates a missing list key
- a call for a missing packaged entry writes nothing
- `entry.yml` writes an entry with all fields and one with the required
  fields only
- marker first, then the `ansible_managed` header, files `root:root 0644`,
  directory `0755`
- calls without changes and with `state: absent` remove the own files, but
  neither the entry of another caller nor the entry without a marker
- `override.yml` and `entry.yml` fail on an existing file of the same name
  without a marker or with the marker of another caller, and leave it
  unchanged
- invalid callers, file names, environment names and values, keys, values
  with line breaks or `;`, a missing `Exec` and an unknown state fail with
  their message and change nothing

## Notes

### Application Environment

Environment variables that work around a driver or toolkit issue belong to
the application, not to the session: `environment.d`, `/etc/environment` or
profile scripts reach every application, and a workaround for one program
changes the behavior of all others. A calling role keeps a
`<role>_environment` mapping (application name to variables) in its
defaults, documents it in its README and passes the variables of one
application to `override.yml` or `entry.yml`. Removing the application from
the mapping removes the override.

### What an Override Does Not Reach

- Applications started from a terminal or by another program do not read
  desktop entries; the environment applies to launches from the desktop
  (menus, launchers, file managers)
- An entry with `DBusActivatable=true` is started through D-Bus by many
  desktops, which ignores `Exec=`; set `DBusActivatable` to `false` with
  `desktop_entries_set` when the environment must apply
- Flatpak applications export their entries to
  `/var/lib/flatpak/exports/share/applications/`; use `flatpak override
  --env=NAME=value` for them instead
- User entries in `~/.local/share/applications/` take precedence over
  `/usr/local/share/applications/`

### Desktop Caches

Most desktops pick up a new or changed entry on their own; a menu that keeps
the old entry needs a new login. The role does not run
`update-desktop-database`.

## References

- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/)
- [ArchWiki: Desktop entries](https://wiki.archlinux.org/title/Desktop_entries)

## License

MIT

## Author

Marc Straube
