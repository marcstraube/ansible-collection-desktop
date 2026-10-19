# marcstraube.desktop.development

Install developer desktop applications: IDEs and editors, database and API
tools, console homebrew toolchains, and per-user editor configuration.

## Description

Installs the graphical side of a development workstation: IDEs and editors
(VS Code, VSCodium, Zed, JetBrains, Arduino), database and API tools, Lua and
QML tooling, Game Boy and devkitPro homebrew toolchains, and per-user editor
settings.

Languages, build tools and CLI tooling live in `marcstraube.common`, which the
base system applies to every host: `python`, `nodejs`, `rust`, `go`, `java`,
`build_tools`, `security_scanners`, the developer tools category of `utils`
and `git`.

## Requirements

- ansible-core >= 2.19
- `community.general` collection (for pacman and user modules)
- `kewlfft.aur` collection (for AUR packages on Arch Linux)

## Supported Platforms

| Platform                  | Notes                                       |
|---------------------------|---------------------------------------------|
| Arch Linux                | Full support including AUR packages         |
| Debian Trixie             | Some IDEs require Flatpak or external repos |
| EL 9 (Rocky, Alma, RHEL)  |                                             |
| EL 10 (Rocky, Alma, RHEL) |                                             |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable              | Default | Description                 |
|-----------------------|---------|-----------------------------|
| `development_enabled` | `true`  | Enable the development role |

### Homebrew Toolchains

#### Gameboy Development

Game Boy / Game Boy Color homebrew tooling. Both tools are AUR-only on
Arch and unpackaged on Debian/RedHat (upstream ships tarball and AppImage
releases), so enabling them there is a no-op that logs a notice.

| Variable                          | Default | Description                                  |
|-----------------------------------|---------|----------------------------------------------|
| `development_gb_gbdk_enabled`     | `false` | Enable the GBDK-2020 cross-compile toolchain |
| `development_gb_gbstudio_enabled` | `false` | Enable the GB Studio visual game maker       |

Platform support:

| Tool      | Arch      | Debian Trixie | EL 9 | EL 10 |
|-----------|-----------|---------------|------|-------|
| GBDK-2020 | yes (AUR) | no            | no   | no    |
| GB Studio | yes (AUR) | no            | no   | no    |

`GBDK-2020` builds from source via the AUR (SDCC-based); `gb-studio-bin`
is the AppImage-derived AUR package.

#### devkitPro (Nintendo Homebrew)

devkitARM / devkitPPC / devkitA64 cross-compiler toolchains for Nintendo
consoles, distributed via devkitPro's own pacman repositories. A master
toggle enables the repo tooling; per-platform toggles select the package
groups to install.

| Variable                                     | Default | Description                            |
|----------------------------------------------|---------|----------------------------------------|
| `development_devkitpro_enabled`              | `false` | Master toggle (keyring + environment)  |
| `development_devkitpro_gba_dev_enabled`      | `false` | Game Boy Advance toolchain (`gba-dev`) |
| `development_devkitpro_nds_dev_enabled`      | `false` | Nintendo DS toolchain (`nds-dev`)      |
| `development_devkitpro_3ds_dev_enabled`      | `false` | Nintendo 3DS toolchain (`3ds-dev`)     |
| `development_devkitpro_gamecube_dev_enabled` | `false` | GameCube toolchain (`gamecube-dev`)    |
| `development_devkitpro_wii_dev_enabled`      | `false` | Wii toolchain (`wii-dev`)              |
| `development_devkitpro_switch_dev_enabled`   | `false` | Switch toolchain (`switch-dev`)        |

Platform support:

| Feature              | Arch | Debian Trixie | EL 9 | EL 10 |
|----------------------|------|---------------|------|-------|
| devkitPro toolchains | yes  | no            | no   | no    |

The `dkp-libs` / `dkp-linux` repos are **registered by
`marcstraube.common.package_management`**, which owns `/etc/pacman.conf`.
Define them in your inventory's `pacman_custom_repositories`. The role
ships the same values in `development_devkitpro_repositories` for
convenience, but `package_management` registers the repos *before* the
`development` role loads its defaults — so a
`{{ development_devkitpro_repositories }}` reference from `group_vars`
does not resolve there. Define the repos inline:

```yaml
# group_vars/<group>/vars.yml
pacman_custom_repositories:
  - name: 'dkp-libs'
    server: 'https://pkg.devkitpro.org/packages'
    key_id: 'BC26F752D25B92CE272E0F44F7FD5492264BB9D0'
    keyserver: 'keyserver.ubuntu.com'
  - name: 'dkp-linux'
    server: 'https://pkg.devkitpro.org/packages/linux/$arch'
    key_id: '032F4C9D0B8FF3BC84019B7862C7609ADA219C60'
    keyserver: 'keyserver.ubuntu.com'
```

devkitPro signs with two master keys (WinterMute and fincs, listed in
`master-keyids` of the `devkitpro-keyring` repository); the repository
databases carry the signature of the second one. pacman keys are global, so
each repository entry imports one of the two. `package_management` imports
and locally signs both; this role installs `devkitpro-keyring`, the `devkit-env` package
(which provides `DEVKITPRO`, `DEVKITARM`, `DEVKITPPC`, `DEVKITA64` and
`PATH` system-wide via `/etc/profile.d/devkit-env.sh`), and the selected
platform groups. The groups share common members (compilers, tools), so
they are install-only — disabling a platform toggle after install does
not uninstall the toolchain. Debian/RedHat are a no-op (a notice is
logged) until the cross-collection alternative-installs strategy lands.

### IDEs and Editors

| Variable                                | Default | Description                     |
|-----------------------------------------|---------|---------------------------------|
| `development_vscode_enabled`            | `false` | Enable VS Code                  |
| `development_vscodium_enabled`          | `true`  | Enable VSCodium                 |
| `development_jetbrains_toolbox_enabled` | `false` | Enable JetBrains Toolbox        |
| `development_phpstorm_enabled`          | `false` | Enable PHPStorm                 |
| `development_zed_enabled`               | `false` | Enable Zed Editor               |
| `development_arduino_ide_enabled`       | `false` | Enable Arduino IDE 2.x          |
| `development_arduino_classic_enabled`   | `false` | Enable classic Arduino IDE 1.x  |

#### VSCode / VSCodium settings

| Variable                      | Default | Description                                   |
|-------------------------------|---------|-----------------------------------------------|
| `development_vscode_settings` | `{...}` | Per-user `settings.json` content (dict)       |
| `development_vscode_argv`     | `{...}` | Per-user `argv.json` (Electron-runtime flags) |

Defaults opt out of editor-core, common Microsoft, and Red Hat extension
telemetry. **Caveat:** extensions (Pylance, C/C++, GitLens, …) have
their own telemetry channels that are not centrally controllable; this
role only covers the editor core, the Electron runtime, and a few
well-known extension switches.

Files are deployed under `~/.config/Code/User/settings.json` and
`~/.vscode/argv.json` (VSCode), and the corresponding `VSCodium` /
`.vscode-oss` paths. The role overwrites these files in `managed` mode —
inventory should populate `development_vscode_settings` with everything
intended, not just deltas.

#### Arduino

Two independent toggles cover the two IDE generations, since their
packaging differs per platform:

| IDE                   | Arch                    | Debian Trixie      | EL 9/10 |
|-----------------------|-------------------------|--------------------|---------|
| Arduino IDE 2.x       | AUR (`arduino-ide-bin`) | no (Flatpak only)  | no      |
| Classic Arduino IDE   | AUR (`arduino`)         | yes (`arduino`)    | no      |

Arduino IDE 2.x on Debian/EL is only distributed as Flatpak
(`cc.arduino.IDE2`) or AppImage; the classic 1.x EPEL package is
orphaned. Enabling an unavailable combination logs a notice and skips.

When either toggle is enabled, the role adds all `development_users`
to the OS-specific serial device groups so boards can be flashed over
USB-serial (`/dev/ttyACM*` / `/dev/ttyUSB*`):

| Platform | Group     | Notes                                                          |
|----------|-----------|----------------------------------------------------------------|
| Arch     | `uucp`    | Required for CH340 chips — `uaccess` alone is not sufficient   |
| Debian   | `dialout` |                                                                |
| EL 9/10  | `dialout` |                                                                |

Membership is append-only: the groups may be required by other tooling,
so disabling the Arduino toggles does not remove users from them. Group
changes take effect at next login.

On Arch the role also deploys a `.desktop` override for Arduino IDE 2.x
under `/usr/local/share/applications/` that redirects stdout/stderr to
`/dev/null`. The IDE main process logs to stdout; launched from a
`.desktop` entry that is a closed pipe, and every write raises an
uncaught EPIPE exception dialog (upstream:
[arduino-ide#2340](https://github.com/arduino/arduino-ide/issues/2340)).
A pacman hook regenerates the override whenever `arduino-ide-bin`
changes the packaged desktop file, so upstream `.desktop` updates are
picked up automatically. Disabling the toggle removes the override,
hook, and generator script.

### Database Tools

| Variable                      | Default | Description    |
|-------------------------------|---------|----------------|
| `development_dbeaver_enabled` | `false` | Enable DBeaver |
| `development_pgadmin_enabled` | `false` | Enable pgAdmin |

### API Tools

| Variable                       | Default | Description     |
|--------------------------------|---------|-----------------|
| `development_postman_enabled`  | `false` | Enable Postman  |
| `development_insomnia_enabled` | `false` | Enable Insomnia |
| `development_bruno_enabled`    | `false` | Enable Bruno    |

### Language Tooling

Per-tool toggles for distro-packaged Lua and QML linters, formatters, and
test frameworks. Each toggle resolves to a `__development_<tool>_package`
variable in `vars/{distro}.yml`. Distros without an upstream package map to
`''`, in which case the install task is a no-op — see "Platform support"
below. Shell and Python tooling live in `marcstraube.common.utils` and
`marcstraube.common.python`.

#### Lua

| Variable                           | Default | Description                          |
|------------------------------------|---------|--------------------------------------|
| `development_lua_stylua_enabled`   | `false` | Enable stylua Lua formatter          |
| `development_lua_luacheck_enabled` | `false` | Enable luacheck Lua linter           |
| `development_lua_busted_enabled`   | `false` | Enable busted Lua test framework     |

#### QML

| Variable                        | Default | Description                                          |
|---------------------------------|---------|------------------------------------------------------|
| `development_qml_tools_enabled` | `false` | Enable Qt6 QML tools (qmllint + qmlformat, same pkg) |

The QML tools are install-only — on Arch they ship in `qt6-declarative`
itself, a core Qt6 library the desktop stack depends on, so disabling the
toggle after install does not uninstall the package.

##### Platform support

| Tool         | Arch | Debian Trixie | EL 9 | EL 10 |
|--------------|------|---------------|------|-------|
| stylua       | yes  | no            | no   | no    |
| luacheck     | yes  | yes           | no   | no    |
| busted       | yes  | yes           | no   | no    |
| qml-tools    | yes  | yes           | yes  | yes   |

### User Configuration

| Variable                       | Default     | Description                                      |
|--------------------------------|-------------|--------------------------------------------------|
| `development_users`            | `[]`        | Users to configure with editor settings          |
| `development_user_config_mode` | `'initial'` | Default mode: `managed` / `initial` / `disabled` |

Each user entry supports:

| Key               | Required | Description                                  |
|-------------------|----------|----------------------------------------------|
| `username`        | yes      | System username                              |
| `mode`            | no       | Per-user override of the global config mode  |

Mode semantics — analog to `marcstraube.desktop.browser`:

| Mode       | First run                       | Subsequent runs                          |
|------------|---------------------------------|------------------------------------------|
| `managed`  | deploy                          | overwrite (always reconcile)             |
| `initial`  | deploy if user is newly created | leave existing user customisations alone |
| `disabled` | skip                            | skip                                     |

## Tags

| Tag                            | Scope                      |
|--------------------------------|----------------------------|
| `development`                  | All role tasks             |
| `development:ides`             | IDE installation tasks     |
| `development:gb-dev`           | Game Boy toolchain tasks   |
| `development:devkitpro`        | devkitPro toolchain tasks  |
| `development:tools`            | Database tools tasks       |
| `development:lua`              | Lua tooling tasks          |
| `development:qml`              | QML tooling tasks          |
| `development:users`            | User configuration tasks   |

## Example Playbook

```yaml
- name: Include development role
  ansible.builtin.include_role:
    name: marcstraube.desktop.development
  tags:
    - development
  when: development_enabled | default(true) | bool
```

### Minimal Development Setup

```yaml
- name: Include development role
  ansible.builtin.include_role:
    name: marcstraube.desktop.development
  vars:
    development_vscodium_enabled: true
    development_users:
      - username: 'johndoe'
  tags:
    - development
  when: development_enabled | default(true) | bool
```

## Testing

```bash
cd roles/development
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## References

- [pipx](https://pipx.pypa.io/) — Install Python applications in isolated environments
- [rustup](https://rustup.rs/) — Rust toolchain installer (used on non-Arch)
- [VSCodium](https://vscodium.com/) — Free/libre Code-OSS binaries (telemetry-free VS Code build)
- [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/) — Manager for JetBrains IDEs
- [Zed](https://zed.dev/) — High-performance multiplayer code editor
- [Arduino IDE 2.x](https://github.com/arduino/arduino-ide) — Arduino IDE, Theia/Electron based
- [Arduino IDE 1.x](https://github.com/arduino/Arduino) — Classic Arduino IDE, Java/Swing based
- [clang](https://clang.llvm.org/) — C/C++ compiler with clang-format, clang-tidy and clangd
- [gdb](https://www.sourceware.org/gdb/) — GNU debugger
- [pkgconf](https://github.com/pkgconf/pkgconf) — Library discovery for build systems
- [codelldb](https://github.com/vadimcn/codelldb) — LLDB debug adapter for VS Code/VSCodium/Zed
- [ccache](https://ccache.dev/) — Compiler cache
- [valgrind](https://valgrind.org/) — Memory and leak debugger
- [cppcheck](https://cppcheck.sourceforge.io/) — C/C++ static analysis
- [bear](https://github.com/rizsotto/Bear) — compile_commands.json generator for non-CMake builds
- [GBDK-2020](https://github.com/gbdk-2020/gbdk-2020) — Game Boy Development Kit (SDCC-based cross-compile toolchain)
- [GB Studio](https://www.gbstudio.dev/) — Visual Game Boy game maker
- [devkitPro](https://devkitpro.org/) — Nintendo console homebrew toolchains (devkitARM/devkitPPC/devkitA64)
- [devkitPro pacman](https://github.com/devkitPro/pacman) — Package manager and repositories for the toolchains
- [shfmt](https://github.com/mvdan/sh) — Shell formatter
- [shellcheck](https://github.com/koalaman/shellcheck) — Shell script static analysis
- [bats-core](https://github.com/bats-core/bats-core) — Bash automated testing system
- [ruff](https://github.com/astral-sh/ruff) — Python linter and formatter
- [uv](https://github.com/astral-sh/uv) — Python package installer and resolver
- [pytest](https://github.com/pytest-dev/pytest) — Python test framework
- [stylua](https://github.com/JohnnyMorganz/StyLua) — Lua formatter
- [luacheck](https://github.com/mpeterv/luacheck) — Lua linter
- [busted](https://github.com/lunarmodules/busted) — Lua test framework
- [Qt qmllint](https://doc.qt.io/qt-6/qtquick-tool-qmllint.html) — QML linter
- [Qt qmlformat](https://doc.qt.io/qt-6/qtquick-tool-qmlformat.html) — QML formatter
- [HTTPie](https://httpie.io/) — Modern HTTP CLI client
- [pre-commit](https://pre-commit.com/) — Multi-language git hook framework
- [direnv](https://direnv.net/) — Per-directory environment variable loader
- [ShellCheck](https://www.shellcheck.net/) — Shell script static analyser
- [Socket CLI](https://socket.dev/cli) — npm dependency supply-chain scanner ([source](https://github.com/SocketDev/socket-cli))

## License

MIT

## Author

Marc Straube
