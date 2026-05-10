# marcstraube.desktop.wine

Install and configure Wine Windows compatibility layer.

## Description

Installs Wine for running Windows applications on Linux. Supports stable and staging
variants (Arch Linux), companion packages (winetricks, wine-mono, wine-gecko), 32-bit
multilib dependencies with automatic GPU Vulkan driver detection, system-wide
environment configuration, and per-user Wine prefix initialization.

## Requirements

- ansible-core >= 2.17
- EPEL repository enabled (for Wine on Rocky Linux 9, managed by
  `marcstraube.common.package_management`)
- Wine is **not available** for EL 10 (no EPEL package exists)

## Supported Platforms

| Platform                  | Notes                                         |
|---------------------------|-----------------------------------------------|
| Arch Linux                | Stable or staging variant, full lib32 support |
| Debian Trixie             | Automatic i386 multiarch enablement           |
| EL 9 (Rocky, Alma, RHEL)  | Via EPEL, 64-bit only (WoW64)                 |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint)
should work but are not actively tested. Use distro-specific vars overrides if needed.

Wine is not available for EL 10 — the role warns and skips on unsupported versions.

## Role Variables

### Role Control

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `wine_enabled` | `true` | Enable the wine role |

### Wine Variant

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `wine_variant` | `'stable'` | Wine variant (`stable` or `staging`, Arch only) |

### Companion Packages

| Variable | Default | Arch | Debian | Rocky 9 | Description |
| -------- | ------- | ---- | ------ | ------- | ----------- |
| `wine_winetricks_enabled` | `true` | yes | yes | no | Install winetricks helper |
| `wine_mono_enabled` | `true` | yes | no | no | Install wine-mono (.NET replacement) |
| `wine_gecko_enabled` | `true` | yes | no | no | Install wine-gecko (IE replacement) |

### 32-bit Support (Arch Linux)

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `wine_lib32_packages` | `[lib32-mesa, ...]` | lib32 packages for 32-bit support |
| `wine_vulkan_driver` | `'auto'` | GPU Vulkan driver (`auto`, `amd`, `intel`, `nvidia`, `none`) |

Debian handles 32-bit automatically via multiarch. EL 9 uses WoW64 mode.

### Environment

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `wine_env_enabled` | `true` | Deploy `/etc/profile.d/wine.sh` |
| `wine_debug` | `'-all'` | Wine debug output level |
| `wine_sync` | `''` | Sync primitive (`ntsync`, `fsync`, `esync`, or empty) |
| `wine_env` | `{}` | Additional environment variables |

### User Configuration

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `wine_user_config_mode` | `'initial'` | Default mode (`managed`/`initial`/`disabled`) |
| `wine_users` | `[]` | Users for Wine prefix initialization |

User config mode semantics:

| Mode       | First run | Subsequent runs                          |
|------------|-----------|------------------------------------------|
| `managed`  | deploy    | overwrite (always reconcile to template) |
| `initial`  | deploy    | leave existing user customisations alone |
| `disabled` | skip      | skip                                     |

`'initial'` is the default: runs `wineboot --init` only when the user's
`{prefix}/system.reg` is absent. Per-user override via `item.mode`
takes precedence over the role-level default.

User entry format:

```yaml
wine_users:
  - username: 'johndoe'
    group: 'johndoe'         # Optional, defaults to username
    mode: 'managed'          # managed/initial/disabled
    prefix: '~/.wine'       # Optional, default WINEPREFIX
    arch: 'win64'            # Optional, win32 or win64
```

## Tags

| Tag | Scope |
| --- | ----- |
| `wine` | All role tasks |
| `wine:install` | Package installation |
| `wine:configure` | Environment and user configuration |

## Example Playbook

```yaml
- name: Include wine role
  ansible.builtin.include_role:
    name: marcstraube.desktop.wine
  tags: [wine]
  when: wine_enabled | default(true) | bool
```

## Testing

```bash
cd roles/wine
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9

## Notes

- Wine has no system-wide configuration files — all configuration is per-user
  inside `$WINEPREFIX` (default `~/.wine`)
- The `wine_variant` variable only affects Arch Linux; Debian and EL always
  install the stable version from distribution repositories
- `wine-staging` conflicts with `wine` on Arch Linux — only one can be installed
- GPU Vulkan driver auto-detection uses `lspci` (same method as
  `marcstraube.common.graphics`)
- NTsync (`wine_sync: 'ntsync'`) requires kernel 6.14+ and Wine 11+ for best
  performance

## References

- [Wine](https://www.winehq.org/) — Compatibility layer for running Windows applications on POSIX systems
- [Wine Wiki](https://gitlab.winehq.org/wine/wine/-/wikis/home) — Documentation, configuration, and troubleshooting
- [Wine AppDB](https://appdb.winehq.org/) — Application compatibility database
- [DXVK](https://github.com/doitsujin/dxvk) — Vulkan-based DirectX 9/10/11 implementation for Wine
- [VKD3D-Proton](https://github.com/HansKristian-Work/vkd3d-proton) — Vulkan-based DirectX 12 implementation
- [winetricks](https://github.com/Winetricks/winetricks) — Helper script for installing common Windows DLLs and apps

## License

MIT

## Author

Marc Straube
