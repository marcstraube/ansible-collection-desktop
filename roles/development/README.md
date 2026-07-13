# marcstraube.desktop.development

Install development tools, IDEs, and programming languages.

## Description

Installs and configures a development environment including version control (Git),
programming languages (Python, Node.js, Rust, Go, Java), build tools, IDEs/editors,
database tools, API testing tools, and miscellaneous CLI utilities. Supports per-user
Git configuration with signing key setup.

## Requirements

- ansible-core >= 2.17
- `community.general` collection (for git_config, pipx, pacman, npm modules)
- `kewlfft.aur` collection (for AUR packages on Arch Linux)
- `marcstraube.common.nodejs` role on non-Arch when enabling tools that
  install via npm (e.g. Socket CLI). The development role itself does
  not install Node.js; `development_nodejs_enabled` is a marker the
  inventory uses to gate the common role.

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

### Version Control

| Variable                         | Default | Description                            |
|----------------------------------|---------|----------------------------------------|
| `development_git_enabled`        | `true`  | Enable git installation                |
| `development_git_lfs_enabled`    | `true`  | Enable git-lfs support                 |
| `development_github_cli_enabled` | `true`  | Enable GitHub CLI (gh)                 |
| `development_gitlab_cli_enabled` | `true`  | Enable GitLab CLI (glab)               |
| `development_git_config`         | `{...}` | Git global configuration key/value map |

### Programming Languages

| Variable                      | Default | Description                           |
|-------------------------------|---------|---------------------------------------|
| `development_python_enabled`  | `true`  | Enable Python installation            |
| `development_python_tools`    | `[]`    | Python tools via pipx (non-Arch)      |
| `development_nodejs_enabled`  | `true`  | Enable Node.js                        |
| `development_rust_enabled`    | `false` | Enable Rust installation              |
| `development_rust_components` | `[]`    | Rust components via rustup (non-Arch) |
| `development_go_enabled`      | `false` | Enable Go installation                |
| `development_java_enabled`    | `false` | Enable Java installation              |
| `development_c_enabled`       | `false` | Enable C/C++ toolchain installation   |

#### C/C++

`development_c_enabled` installs the core C/C++ tooling block: `clang`
(with `clang-format`, `clang-tidy` and the `clangd` LSP server), `gdb`
and `pkgconf`. Fine-grained toggles add optional helpers:

| Variable                          | Default | Description                                            |
|-----------------------------------|---------|--------------------------------------------------------|
| `development_c_codelldb_enabled`  | `false` | Enable codelldb LLDB debug adapter (Arch AUR only)     |
| `development_c_ccache_enabled`    | `false` | Enable ccache compiler cache                           |
| `development_c_valgrind_enabled`  | `false` | Enable valgrind memory and leak debugger               |
| `development_c_cppcheck_enabled`  | `false` | Enable cppcheck static analysis                        |
| `development_c_bear_enabled`      | `false` | Enable bear (`compile_commands.json` for non-CMake)    |

Platform support:

| Tool       | Arch      | Debian Trixie | EL 9       | EL 10      |
|------------|-----------|---------------|------------|------------|
| core block | yes       | yes           | yes        | yes        |
| codelldb   | yes (AUR) | no            | no         | no         |
| ccache     | yes       | yes           | yes (EPEL) | yes (EPEL) |
| valgrind   | yes       | yes           | yes\*      | yes\*      |
| cppcheck   | yes       | yes           | yes (EPEL) | yes (EPEL) |
| bear       | yes       | yes           | yes (EPEL) | no         |

On Debian the core block additionally installs the separate `clangd`,
`clang-format` and `clang-tidy` packages; on EL they ship in
`clang-tools-extra`. `codelldb` is the LLDB debug adapter used by
VS Code/VSCodium/Zed for native debugging; upstream distributes only a
VSIX archive, so it is AUR-only. `bear` is not packaged in EPEL 10.
Enabling an unavailable combination is a no-op (codelldb logs a notice).

\* On EL, `valgrind` ships with the `@Development Tools` group pulled in by
the build-tools section, so its own toggle is a no-op there — it is present
whenever the build tools are installed.

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
The role ships the ready-made repo definitions in
`development_devkitpro_repositories` (including the signing key); wire
them into your inventory once:

```yaml
# group_vars/workstations/vars.yml
pacman_custom_repositories: "{{ development_devkitpro_repositories }}"
# ...or append to an existing list:
#   pacman_custom_repositories: "{{ my_repos + development_devkitpro_repositories }}"
```

`package_management` then imports and locally signs the devkitPro master
key; this role installs `devkitpro-keyring`, the `devkit-env` package
(which provides `DEVKITPRO`, `DEVKITARM`, `DEVKITPPC`, `DEVKITA64` and
`PATH` system-wide via `/etc/profile.d/devkit-env.sh`), and the selected
platform groups. The groups share common members (compilers, tools), so
they are install-only — disabling a platform toggle after install does
not uninstall the toolchain. Debian/RedHat are a no-op (a notice is
logged) until the cross-collection alternative-installs strategy lands.

### Build Tools

| Variable                    | Default | Description                      |
|-----------------------------|---------|----------------------------------|
| `development_make_enabled`  | `true`  | Enable make and core build tools |
| `development_cmake_enabled` | `true`  | Enable cmake                     |
| `development_meson_enabled` | `true`  | Enable meson                     |
| `development_ninja_enabled` | `true`  | Enable ninja                     |

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
| `development_httpie_enabled`   | `true`  | Enable httpie   |
| `development_postman_enabled`  | `false` | Enable Postman  |
| `development_insomnia_enabled` | `false` | Enable Insomnia |
| `development_bruno_enabled`    | `false` | Enable Bruno    |

### Misc Tools

| Variable                         | Default | Description                        |
|----------------------------------|---------|------------------------------------|
| `development_jq_enabled`         | `true`  | Enable jq JSON processor           |
| `development_yq_enabled`         | `true`  | Enable yq YAML processor           |
| `development_direnv_enabled`     | `true`  | Enable direnv directory-based envs |
| `development_pre_commit_enabled` | `true`  | Enable pre-commit git hooks        |

### Security Tooling

| Variable                         | Default | Description                                          |
|----------------------------------|---------|------------------------------------------------------|
| `development_socket_cli_enabled` | `false` | Enable Socket CLI (npm supply-chain scanner)         |

Socket CLI is an npm-native tool. Arch installs the AUR package
`socket-cli` (which wraps the upstream npm package); Debian and EL
install the `socket` npm package globally via `community.general.npm`.
On non-Arch, `marcstraube.common.nodejs` must be applied before this
role to provide `npm`.

### Language Tooling

Per-tool toggles for distro-packaged linters, formatters, and test frameworks.
Each toggle resolves to a `__development_<tool>_package` variable in
`vars/{distro}.yml`. Distros without an upstream package map to `''`, in which
case the install task is a no-op — see "Platform support" below.

For tools installed via a language package manager (`pipx`, `rustup`) the
role uses the free-form lists `development_python_tools` and
`development_rust_components` under "Programming Languages" above.

#### Shell

`shfmt` and `shellcheck` cover multiple shell dialects (POSIX sh, bash,
dash, ksh, mksh); `bats-core` is bash-specific.

| Variable                                 | Default | Description                          |
|------------------------------------------|---------|--------------------------------------|
| `development_shell_shfmt_enabled`        | `false` | Enable shfmt shell formatter         |
| `development_shell_shellcheck_enabled`   | `true`  | Enable shellcheck shell linter       |
| `development_shell_bats_enabled`         | `false` | Enable bats-core Bash test framework |

#### Python Tooling

| Variable                          | Default | Description                                     |
|-----------------------------------|---------|-------------------------------------------------|
| `development_python_ruff_enabled` | `false` | Enable ruff Python linter and formatter         |
| `development_python_uv_enabled`   | `false` | Enable uv Python package installer and resolver |

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

##### Platform support

| Tool         | Arch | Debian Trixie | EL 9 | EL 10 |
|--------------|------|---------------|------|-------|
| shfmt        | yes  | yes           | no   | no    |
| shellcheck   | yes  | yes           | yes  | yes   |
| bats         | yes  | yes           | yes  | yes   |
| ruff         | yes  | no            | no   | yes   |
| uv           | yes  | no            | no   | yes   |
| stylua       | yes  | no            | no   | no    |
| luacheck     | yes  | yes           | no   | no    |
| busted       | yes  | yes           | no   | no    |
| qml-tools    | yes  | yes           | yes  | yes   |

### User Configuration

| Variable                       | Default     | Description                                      |
|--------------------------------|-------------|--------------------------------------------------|
| `development_users`            | `[]`        | Users to configure with git + IDE settings       |
| `development_user_config_mode` | `'initial'` | Default mode: `managed` / `initial` / `disabled` |

Each user entry supports:

| Key               | Required | Description                                  |
|-------------------|----------|----------------------------------------------|
| `username`        | yes      | System username                              |
| `mode`            | no       | Per-user override of the global config mode  |
| `git_name`        | no       | Git user.name                                |
| `git_email`       | no       | Git user.email                               |
| `git_signing_key` | no       | GPG signing key ID                           |

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
| `development:git`              | Version control tasks      |
| `development:languages`        | Programming language tasks |
| `development:build`            | Build tools tasks          |
| `development:ides`             | IDE installation tasks     |
| `development:tools`            | Misc tools tasks           |
| `development:shell`            | Shell tooling tasks        |
| `development:python-tooling`   | Python tooling tasks       |
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
    development_rust_enabled: true
    development_users:
      - username: 'johndoe'
        git_name: 'John Doe'
        git_email: 'john@example.com'
        git_signing_key: '0x1234567890ABCDEF'
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

- [Git](https://git-scm.com/) — Distributed version control system
- [GitHub CLI](https://cli.github.com/) — `gh` command-line tool for GitHub
- [glab](https://gitlab.com/gitlab-org/cli) — GitLab CLI
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
