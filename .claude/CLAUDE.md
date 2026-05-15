# Claude Code — marcstraube.desktop Collection

## Overview

Desktop workstation roles for Arch Linux and Debian Trixie — desktop environments,
display managers, browsers, development tools, multimedia, and productivity software.

## Coding Standards (ansible-core 2.17+)

- **Facts:** `ansible_facts['os_family']` — never `ansible_os_family` (deprecated)
- **Modules:** Always FQCN (`ansible.builtin.*`, `community.general.*`, `kewlfft.aur.*`)
- **Roles:** `ansible.builtin.include_role` — never `import_role`
- **Tasks:** `ansible.builtin.include_tasks` — never `import_tasks` for conditional dispatch
- **Tag propagation:** Always `apply: tags:` when using `include_tasks` inside blocks
- **Variables:** `<role>_<setting>`, internal: `__<role>_<setting>` (double underscore)
- **Booleans:** `<role>_enabled` with `default(true/false) | bool`
- **Templates:** `ansible_managed | comment` header
- **Comments:** English only

Full reference with YAML quoting rules: see infra project `.claude/CLAUDE.md`.

## Role Conventions

Same conventions as `marcstraube.common` — see that collection's CLAUDE.md for
directory structure, variable naming, task patterns, and template rules.

## Key Roles

| Role | Purpose | Notes |
| ------ | ------- | ------- |
| `desktop_environment` | Hyprland, Sway, GNOME, KDE, i3, XFCE | `desktop_environment_list` for multi-DE |
| `display_manager` | greetd, GDM, SDDM, LightDM | Configurable greeter + compositor |
| `browser` | Firefox, LibreWolf, Chromium, Brave | Hardening, extension policies |
| `keepassxc` | Password manager | Secret service, browser integration |
| `development` | Languages, build tools, IDEs, Git | Container tools (Podman) |
| `ai` | Claude Code, Ollama, Gemini CLI | API key management |
| `pipewire` | Audio stack | Replaces PulseAudio |
| `bluetooth` | BlueZ configuration | Security timeouts, MAC privacy |
| `terminal` | Ghostty, Alacritty, Kitty, Foot | Per-user config |
| `shell` | Zsh, Fish, Bash | Oh-My-Zsh, plugins |
| `office` | LibreOffice, Thunderbird, Obsidian | Language packs |

## Display Manager — Greeter Architecture

The `display_manager` role supports configurable greeters:

- **TUI greeters** (`agreety`, `tuigreet`): Run directly, no compositor needed
- **Graphical greeters** (`gtkgreet`, `regreet`): Need a compositor wrapper

Default is `agreety` (built-in, no dependencies). When using graphical greeters,
set `display_manager_greetd_greeter_compositor` to `hyprland` or `sway`.

The role deploys a minimal compositor config (`greetd-hyprland.conf` or
`greetd-sway.conf`) that launches the greeter and exits.

## Playbooks

| Playbook                   | Purpose                      | Hosts          |
| -------------------------- | ---------------------------- | -------------- |
| `desktop_workstation.yml`  | Full desktop setup           | `workstations` |
| `laptop.yml`               | Laptop-specific additions    | `laptops`      |

### Tag Usage

All `include_tasks` in roles use `apply: tags:` for proper `--tags` filtering:

```yaml
- name: Include feature
  ansible.builtin.include_tasks:
    file: feature.yml
    apply:
      tags:
        - mytag
  tags:
    - mytag
```

## Security

- Vault files (`vault.yml`) are never accessed — only `vault.yml.example` templates
- Use `{{ vault_* }}` variable references, never hardcode secrets
- See root `.claude/CLAUDE.md` for vault protection rules
