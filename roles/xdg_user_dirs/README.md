# marcstraube.desktop.xdg_user_dirs

Install `xdg-user-dirs` and create the standard user directories per user.

## Description

Manages the per-user XDG base-directory map (`~/.config/user-dirs.dirs`)
and the directories themselves (`~/Documents`, `~/Downloads`,
`~/Projects`, …). Names are localized by the user's chosen locale
through `xdg-user-dirs-update`. A freeze file (`~/.config/user-dirs.conf`
with `enabled=False`) prevents desktop-environment login hooks from
silently rewriting the map between Ansible runs.

Works on Arch Linux, Debian Trixie, and EL 9/10 — `xdg-user-dirs` is in
all three package repositories.

## Requirements

- ansible-core >= 2.17
- Target host's chosen UTF-8 locale must be generated (`/etc/locale.gen`
  enabled and `locale-gen` run); the `marcstraube.common.base` role
  handles this.

## Supported Platforms

| Platform      | Notes                                  |
| ------------- | -------------------------------------- |
| Arch Linux    | `xdg-user-dirs` package, native locale |
| Debian Trixie | same package                           |
| EL 9 / EL 10  | same package                           |

## Role Variables

### Role Control

| Variable                | Default | Description         |
| ----------------------- | ------- | ------------------- |
| `xdg_user_dirs_enabled` | `true`  | Enable/disable role |

### Localization

| Variable               | Default         | Description                                 |
| ---------------------- | --------------- | ------------------------------------------- |
| `xdg_user_dirs_locale` | `'en_US.UTF-8'` | Locale used when generating directory names |

The locale's `.po` data ships inside the `xdg-user-dirs` package, so
the role does not need to install separate translation packs.

### Extra (custom) directories

| Variable              | Default | Description                                        |
| --------------------- | ------- | -------------------------------------------------- |
| `xdg_user_dirs_extra` | `{}`    | Additional XDG entries beyond the package defaults |

Format: dict with the XDG key (without the `XDG_` prefix and `_DIR`
suffix) as key, relative path under `$HOME` as value:

```yaml
xdg_user_dirs_extra:
  MEDIA: 'Medien'
  BACKUP: 'Sicherungen'
```

Each entry is added via `lineinfile` with an idempotent regex on
`XDG_<KEY>_DIR=`. If a future `xdg-user-dirs` release ships the same
key as a default, the line is replaced in place rather than duplicated.

### Skipping standard entries

| Variable             | Default | Description                                               |
| -------------------- | ------- | --------------------------------------------------------- |
| `xdg_user_dirs_skip` | `[]`    | XDG keys to remove from `user-dirs.dirs` (no dir created) |

```yaml
xdg_user_dirs_skip:
  - TEMPLATES
  - PUBLICSHARE
```

Removes those `XDG_<KEY>_DIR=` lines from `~/.config/user-dirs.dirs`
after `xdg-user-dirs-update` wrote them, and skips directory creation
for the dropped keys. Locale translation of the kept entries is
unaffected. Default empty = create everything `xdg-user-dirs` ships,
including future additions like `PROJECTS` (added in 0.20).

### User configuration

| Variable                         | Default     | Description                                       |
| -------------------------------- | ----------- | ------------------------------------------------- |
| `xdg_user_dirs_users`            | `[]`        | Users to configure                                |
| `xdg_user_dirs_user_config_mode` | `'initial'` | Default mode: `managed` / `initial` / `disabled`  |
| `xdg_user_dirs_mode`             | `'0755'`    | Mode of created dirs (`'0700'` for private homes) |

Per-user entry:

```yaml
xdg_user_dirs_users:
  - username: 'johndoe'
    mode: 'managed'   # optional, overrides the global default
```

Mode semantics — identical to `marcstraube.desktop.browser` and
`marcstraube.desktop.development`:

| Mode       | First run                       | Subsequent runs                                        |
| ---------- | ------------------------------- | ------------------------------------------------------ |
| `managed`  | deploy                          | re-run `xdg-user-dirs-update --force`, re-apply extras |
| `initial`  | deploy if user is newly created | leave existing user-dirs.dirs alone                    |
| `disabled` | skip                            | skip                                                   |

## What the freeze actually does

`~/.config/user-dirs.conf` with `enabled=False` blocks the
**auto-triggered** `xdg-user-dirs-update` calls (typical desktop
environments run it on login). This protects both the Ansible-managed
state and any manual edits the user makes to `~/.config/user-dirs.dirs`
between Ansible runs.

It does **not** block:

- Manual edits via text editor.
- Explicit `xdg-user-dirs-update --set <DIR> <path>` calls (a deliberate
  user action).
- `xdg-user-dirs-update --force` (operator override; this is what the
  role itself uses, so re-runs still work).

So in `mode: initial`, users keep full ownership of the file after the
initial deploy; the freeze just prevents an external tool from
clobbering their changes on every login.

## Tags

| Tag                     | Scope                  |
| ----------------------- | ---------------------- |
| `xdg_user_dirs`         | All role tasks         |
| `xdg_user_dirs:install` | Package installation   |
| `xdg_user_dirs:users`   | Per-user configuration |

## Example Playbook

```yaml
- name: Workstation
  hosts: workstations
  tasks:
    - name: Include xdg_user_dirs role
      ansible.builtin.include_role:
        name: marcstraube.desktop.xdg_user_dirs
      tags: [xdg_user_dirs]
      when: xdg_user_dirs_enabled | default(true) | bool
```

Inventory example for a German workstation:

```yaml
xdg_user_dirs_locale: 'de_DE.UTF-8'
xdg_user_dirs_extra:
  MEDIA: 'Medien'
xdg_user_dirs_users:
  - username: 'marc'
```

## Testing

```bash
cd roles/xdg_user_dirs
molecule test
```

Driver: Podman. Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10.

## References

- [freedesktop.org xdg-user-dirs][upstream] — upstream spec and tool
- [xdg-user-dirs 0.20 release notes][projects-blog] — background on the
  new `PROJECTS` default

[upstream]: https://www.freedesktop.org/wiki/Software/xdg-user-dirs/
[projects-blog]: https://blog.tenstral.net/2026/04/hello-projects-directory.html

## License

MIT

## Author

Marc Straube
