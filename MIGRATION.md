# Migration Guide

Upgrade guide for users of `marcstraube.desktop`. Each release with
breaking changes adds a section here with before/after inventory
snippets. For the full list of changes per release, see
[CHANGELOG.md](CHANGELOG.md).

## v2.0.0 (unreleased)

### `development_shellcheck_enabled` renamed (#116)

shellcheck moves from "Misc Tools" into the new `# Language Tooling`
section under `# Shell`, alongside `shfmt` and `bats`. The toggle is
renamed accordingly. Hard rename, no fallback.

| Old name                          | New name                                |
|-----------------------------------|-----------------------------------------|
| `development_shellcheck_enabled`  | `development_shell_shellcheck_enabled`  |

#### Before

```yaml
development_shellcheck_enabled: true
```

#### After

```yaml
development_shell_shellcheck_enabled: true
```

### Boolean toggles renamed to follow `_enabled` convention (#43)

Three logic-gate booleans were renamed to match the project's
`<role>_<setting>_enabled` convention. Hard rename, no fallback.

| Role        | Old name                       | New name                                  |
|-------------|--------------------------------|-------------------------------------------|
| `bluetooth` | `bluetooth_deprecated_tools`   | `bluetooth_deprecated_tools_enabled`      |
| `bluetooth` | `bluetooth_obex`               | `bluetooth_obex_enabled`                  |
| `tuxedo`    | `tuxedo_warn_conflicts`        | `tuxedo_warn_conflicts_enabled`           |

The other `bluetooth_*` booleans (`auto_enable`, `always_pairable`,
`name_resolving`, `fast_connectable`) are direct config-file mirrors
rendered verbatim into `bluetooth.conf` — they stay as-is per
convention.

#### Before

```yaml
bluetooth_deprecated_tools: true
bluetooth_obex: false
tuxedo_warn_conflicts: true
```

#### After

```yaml
bluetooth_deprecated_tools_enabled: true
bluetooth_obex_enabled: false
tuxedo_warn_conflicts_enabled: true
```

### Deprecated CLI file manager variables removed (#41)

The terminal file-manager variables were migrated to
`marcstraube.common.utils` in v1.x with deprecation warnings. v2.0.0
removes the fallback definitions, install tasks, and OS vars from the
desktop `filemanagers` role. Use the `utils_filemgr_*_enabled` toggles
in `marcstraube.common.utils` instead.

| Old name (desktop)             | New name (`marcstraube.common.utils`)  |
|--------------------------------|----------------------------------------|
| `filemanagers_vifm_enabled`    | `utils_filemgr_vifm_enabled`           |
| `filemanagers_mc_enabled`      | `utils_filemgr_mc_enabled`             |
| `filemanagers_ranger_enabled`  | `utils_filemgr_ranger_enabled`         |
| `filemanagers_nnn_enabled`     | `utils_filemgr_nnn_enabled`            |
| `filemanagers_lf_enabled`      | `utils_filemgr_lf_enabled`             |

The desktop `filemanagers` role retains its GUI file managers
(`filemanagers_thunar_enabled`, etc.) and the umbrella
`filemanagers_enabled`.

#### Before

```yaml
filemanagers_ranger_enabled: true
filemanagers_lf_enabled: true
```

#### After

```yaml
# In group_vars / host_vars covering marcstraube.common.utils consumers:
utils_filemgr_ranger_enabled: true
utils_filemgr_lf_enabled: true
```

### `shell` role default changed from `zsh` to `bash` (#42)

`bash` is the POSIX-style shell shipped with every supported
distribution and works without additional packages or per-user
configuration. Defaulting to `bash` makes the role usable on a fresh
host with zero overrides.

| Variable             | v1.x default | v2.0.0 default |
|----------------------|--------------|----------------|
| `shell_default`      | `'zsh'`      | `'bash'`       |
| `shell_zsh_enabled`  | `true`       | `false`        |

#### Before

```yaml
# v1.x: zsh was picked up by default
shell_default: 'zsh'        # implicit
shell_zsh_enabled: true     # implicit
```

#### After

```yaml
# v2.0.0 default: bash. To restore previous behaviour:
shell_default: 'zsh'
shell_zsh_enabled: true
```

Note: the `shell` role itself moved to `marcstraube.common` in #118 —
the variables above are now read from the common collection. See the
shell-role-relocation section further down.

### `keepassxc_secret_service_global` replaced by enum `_scope` (#44)

The boolean form had two issues: the name read "is this global?" but
the truthy value was the unusual case, and a `_global_enabled: false`
would have parsed as "not-global is disabled". Replaced with the
project's established enum pattern (`'user'` / `'global'`).

Missing or invalid values fail fast with an assertion rather than
silently falling back.

#### Before

```yaml
keepassxc_secret_service_global: false   # per-user
# or
keepassxc_secret_service_global: true    # global
```

#### After

```yaml
keepassxc_secret_service_scope: 'user'    # default; ~/.local/share/dbus-1/services/  # pragma: allowlist secret
# or
keepassxc_secret_service_scope: 'global'  # /usr/local/share/dbus-1/services/  # pragma: allowlist secret
```

### `browser_user_config_mode` default changed from `managed` to `initial` (#55)

Browser settings are typically adjusted by the user; the previous
`'managed'` default silently overwrote those adjustments on every
Ansible run. The new `'initial'` default deploys on first run and
preserves user customisations afterwards.

| Variable                       | v1.x default | v2.0.0 default |
|--------------------------------|--------------|----------------|
| `browser_user_config_mode`     | `'managed'`  | `'initial'`    |

#### Before

```yaml
# v1.x: role would reconcile browser user files on every run
browser_user_config_mode: 'managed'
```

#### After

```yaml
# v2.0.0 default: deployed once, then user-owned.
# Restore the previous behaviour with:
browser_user_config_mode: 'managed'
```

### `shell_user_config_mode` default flipped + starship config now actually deploys (#58)

Two changes ship together:

1. `shell_user_config_mode` default flipped from `'managed'` to
   `'initial'`. Same rationale as the browser flip: user customisations
   of `.zshrc` / Oh My Zsh / `starship.toml` are now preserved on
   subsequent runs by default.
2. `shell_starship_config_enabled` and `shell_starship_preset` were
   defined in `defaults/main.yml` but never wired into tasks (no-op).
   This PR adds `tasks/starship.yml` which actually deploys
   `~/.config/starship.toml` from a preset.

| Variable                          | v1.x default        | v2.0.0 default              |
|-----------------------------------|---------------------|-----------------------------|
| `shell_user_config_mode`          | `'managed'`         | `'initial'`                 |
| `shell_starship_config_enabled`   | `false` (was no-op) | `false` (now actually used) |

#### Before

```yaml
# v1.x: shell user config reconciled every run; starship_preset ignored
shell_user_config_mode: 'managed'
shell_starship_config_enabled: true    # silently no-op
shell_starship_preset: 'nerd-font'     # silently no-op
```

#### After

```yaml
# v2.0.0: opt in explicitly for the previous reconcile-every-run behaviour
shell_user_config_mode: 'managed'

# starship config now actually deploys ~/.config/starship.toml
shell_starship_config_enabled: true
shell_starship_preset: 'nerd-font-symbols'   # validated against starship preset --list
```

Valid `shell_starship_preset` values are asserted at task start;
invalid names fail fast with a clear error. See the role README for
the full list.

Note: the `shell` role itself moved to `marcstraube.common` in #118 —
the variables above are now read from the common collection.

### `keepassxc_user_config_mode` default flipped + `initial` mode now implemented (#59)

The old `tasks/configure.yml` only guarded against `mode == 'disabled'`,
so `'initial'` behaved identically to `'managed'`: every run
overwrote the user's `keepassxc.ini`. The promised "deploy only on
first creation" semantics were never implemented.

v2.0.0 implements per-user stat + skip logic for `'initial'`-mode users
when `~/.config/keepassxc/keepassxc.ini` already exists. The default is
also flipped to `'initial'` for the same reason as browser/shell.

| Variable                          | v1.x default | v2.0.0 default |
|-----------------------------------|--------------|----------------|
| `keepassxc_user_config_mode`      | `'managed'`  | `'initial'`    |

| Mode        | First run | Subsequent runs                          |
|-------------|-----------|------------------------------------------|
| `managed`   | deploy    | overwrite (always reconcile to template) |
| `initial`   | deploy    | leave existing user customisations alone |
| `disabled`  | skip      | skip                                     |

#### Before

```yaml
# v1.x: 'initial' mode set, behaviour was actually 'managed' (bug)
keepassxc_user_config_mode: 'initial'
```

#### After

```yaml
# v2.0.0: 'initial' is the default AND actually preserves user edits.
# To restore the previous always-reconcile behaviour:
keepassxc_user_config_mode: 'managed'
```

### `wine_user_config_mode` default flipped + `initial` mode now implemented (#60)

Same shape as #59 for the `wine` role: `'initial'` mode silently
behaved like `'managed'` (the user include fired every run regardless),
heavy work was first-run-only by accident because `wineboot --init`
uses `creates:`. v2.0.0 implements proper per-user gating and flips
the default.

| Variable                  | v1.x default | v2.0.0 default |
|---------------------------|--------------|----------------|
| `wine_user_config_mode`   | `'managed'`  | `'initial'`    |

#### Before

```yaml
# v1.x: 'initial' silently behaved like 'managed' at the include gate
wine_user_config_mode: 'initial'
```

#### After

```yaml
# v2.0.0: 'initial' is the default and properly skips the user
# include once the wine prefix exists. To reconcile every run:
wine_user_config_mode: 'managed'
```

### `wayland_utils` — `swww` renamed to `awww` + matugen toggle (#93)

The wallpaper-daemon mapping key and the upstream binary name changed
from `swww` to `awww`. Inventories that pin the wallpaper daemon or
reference it from Hyprland autostart must update.

A new toggle `wayland_utils_matugen_enabled` (default `false`) opts
into Material You colour generation via the `matugen` tool.

#### Before

```yaml
wayland_utils_wallpaper: 'swww'

desktop_environment_hyprland_autostart:
  - "swww init"
```

#### After

```yaml
wayland_utils_wallpaper: 'awww'

desktop_environment_hyprland_autostart:
  - "awww init"
```

### `browser` — Firefox locked prefs migrated to `policies.json` Preferences policy (#104)

`browser_firefox_preferences` was previously deployed by **both**
mechanisms — `lockPref()` in `firefox.cfg` (system-wide locked) **and**
`user_pref()` in `<profile>/user.js` (per-user, overridable). Both
iterated over the same variable, so every entry was silently
double-deployed, the locked form won, and there was no way to express
"deploy as a default the user can change".

v2.0.0 removes `firefox.cfg` + `autoconfig.js` entirely. Locked prefs
now go into `browser_firefox_policy_settings.Preferences` (Mozilla's
official enterprise API); non-whitelisted user-overridable prefs stay
in `browser_firefox_preferences` and deploy via `user.js` only.

`browser_firefox_preferences` is **empty by default** in v2.0.0 (the
11 v1.x defaults were either covered by other policies or matched
Firefox built-in defaults).

#### Before

```yaml
browser_firefox_preferences:
  # Silently deployed BOTH as lockPref() in firefox.cfg AND as
  # user_pref() in user.js — the locked form won.
  network.prefetch-next: false
  network.dns.disablePrefetch: true
  privacy.resistFingerprinting: true
```

#### After

```yaml
# Lock-intended entries that Mozilla's whitelist supports move here:
browser_firefox_policy_settings:
  Preferences:
    network.prefetch-next:
      Value: false
      Status: locked
    network.dns.disablePrefetch:
      Value: true
      Status: locked

# Non-whitelisted prefs stay here and deploy as user.js (overridable):
browser_firefox_preferences:
  privacy.resistFingerprinting: true
```

The Mozilla `Preferences` policy whitelist is the authoritative list of
locked-pref-supported keys — see
[Policies.sys.mjs](https://github.com/mozilla/gecko-dev/blob/master/browser/components/enterprisepolicies/Policies.sys.mjs).

LibreWolf does **not** gain a `Preferences` policy — its packaged
`librewolf.cfg` hardening already covers the migrated prefs via
`defaultPref`.

The role does not remove pre-existing `firefox.cfg` /
`autoconfig.js` / `user.js` from upgraded hosts (intentional — operator
opt-in cleanup). Manual cleanup if desired:

```bash
sudo rm /usr/lib/firefox/firefox.cfg /usr/lib/firefox/defaults/pref/autoconfig.js
rm ~/.mozilla/firefox/<profile>.default-release/user.js
```

### `keepassxc` — autostart switched to XDG, ini defaults expanded (#111)

The per-user systemd service template for KeePassXC autostart is
removed. Autostart now uses the native XDG entry at
`~/.config/autostart/org.keepassxc.KeePassXC.desktop`, eliminating
drift between role state and KeePassXC's GUI autostart checkbox.

The template mirrors KeePassXC's GUI-written file (including
`X-GNOME-Autostart-Delay`, `X-KDE-autostart-after=panel`,
`X-LXQt-Need-Tray=true`). `item.delay` maps to
`X-GNOME-Autostart-Delay`. `GenericName` is locale-aware: per-user
`lang` > host-level `keepassxc_locale` (default `en_US.UTF-8`) >
English fallback.

Five settings are added to `keepassxc_config` defaults:
`General.BackupBeforeSave`, `General.UseAtomicSaves`,
`GUI.MinimizeOnClose`, `GUI.MinimizeOnStartup`,
`GUI.TrayIconAppearance`.

#### Before

```yaml
# v1.x: per-user systemd user service deployed
keepassxc_autostart_enabled: true
```

#### After

```yaml
# v2.0.0: per-user XDG autostart entry deployed (no inventory change
# needed). Existing hosts should clean up the old service unit:
#   rm ~/.config/systemd/user/keepassxc.service
# The role does not handle that automatically (v2.0.0 clean break).
keepassxc_autostart_enabled: true
```

### `shell` role relocated to `marcstraube.common` (#118)

The `shell` role moved verbatim from `marcstraube.desktop` to
`marcstraube.common`, alongside `multiplexer`, as CLI tooling that
applies to all hosts (workstations and servers) rather than only
desktops. All `shell_*` inventory variables keep their names; only the
FQCN changes.

The role is now included automatically by
`marcstraube.common.base_system`, so most desktop consumers only need
to drop any direct desktop-collection reference if they had one.

#### Before

```yaml
- hosts: workstations
  roles:
    - marcstraube.desktop.shell
```

#### After

```yaml
- hosts: all
  roles:
    - marcstraube.common.shell
```

### `ai` ComfyUI install switched to AUR on Arch (#121)

The `ai` role installs ComfyUI via a different strategy per OS family
in v2.0.0:

- **Arch Linux**: the AUR `comfyui` package via `kewlfft.aur.aur`.
  The PKGBUILD owns the install dir (`/opt/comfyui`), the service
  user (`comfy`), the Python venv, the PyTorch wheel selection
  (driven by `COMFYUI_GPU={cuda,rocm,cpu}` mapped from
  `ai_comfyui_gpu`), and the systemd unit.
- **Debian / Rocky Linux**: from-source manual install (clone the
  upstream repo, build a Python venv, install PyTorch wheels). The
  flow itself is unchanged from v1.x; PR #121 also ships two
  structural bugfixes to the manual path that previously broke fresh
  installs — the missing `ansible.builtin.group` task (the service
  group is now created before the service user), and the service
  user's home decoupled from the install directory via the new
  `ai_comfyui_home` variable (default `/var/lib/comfyui`) so
  `become_user`'s `~/.ansible/tmp/` no longer pollutes the git-clone
  target.

#### Variable semantics change on Arch

The following inventory variables are **no longer honored** on Arch —
the AUR package determines those values:

- `ai_comfyui_user` — AUR-fixed to `comfy`
- `ai_comfyui_group` — AUR-fixed to `comfy`
- `ai_comfyui_install_dir` — AUR-fixed to `/opt/comfyui`
- `ai_comfyui_home` — AUR-fixed to `/var/lib/comfyui`

These variables still apply on the manual install path (Debian / Rocky).

#### Before

```yaml
# v1.x on Arch: manual install honored these
ai_comfyui_install_dir: '/srv/comfyui'   # would install to /srv/comfyui
ai_comfyui_user: 'sdadmin'               # would create that user
```

#### After

```yaml
# v2.0.0 on Arch: AUR install ignores those overrides; remove them.
# The AUR-fixed paths (/opt/comfyui, user `comfy`) are used regardless.
# On Debian/Rocky the overrides above still take effect.

ai_comfyui_enabled: true
ai_comfyui_gpu: 'amd'   # nvidia / amd / cpu — maps to COMFYUI_GPU
```

If the previous manual install left files at a non-default location
(e.g. `/srv/comfyui` with a custom user), clean those up by hand before
the first v2.0.0 run on the host — the role does not migrate existing
installs.
