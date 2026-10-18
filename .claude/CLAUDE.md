# Claude Code — marcstraube.desktop Collection

## Overview

Desktop workstation roles for Arch Linux and Debian Trixie — desktop environments,
display managers, browsers, development tools, multimedia, and productivity software.

## Coding Standards (ansible-core 2.19+)

- **Facts:** `ansible_facts['os_family']` — never `ansible_os_family` (deprecated)
- **Modules:** Always FQCN (`ansible.builtin.*`, `community.general.*`, `kewlfft.aur.*`)
- **Roles:** `ansible.builtin.include_role` — never `import_role`
- **Tasks:** `ansible.builtin.include_tasks` — never `import_tasks` for conditional dispatch
- **Tag propagation:** Always `apply: tags:` when using `include_tasks` inside blocks
- **Variables:** `<role>_<setting>`, internal: `__<role>_<setting>` (double underscore)
- **Booleans:** `<role>_enabled | bool` — the role default in `defaults/main.yml`
  is the single source of truth (see [Role toggles](#role-toggles))
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
| `ai` | Claude Code, Ollama, Antigravity | API key management |
| `pipewire` | Audio stack | Replaces PulseAudio |
| `bluetooth` | BlueZ configuration | Security timeouts, MAC privacy |
| `terminal` | Ghostty, Alacritty, Kitty, Foot | Per-user config |
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

#### Sub-tags must be self-contained

A role exposes sub-tags (`<role>:<phase>`, e.g. `browser:configure`) so a single
stage can be run in isolation. For that to work, two rules apply:

1. **Entry playbooks import roles statically.** `playbooks/tasks/desktop_workstation.yml`
   uses `import_role` (not `include_role`) for every role. A dynamic `include_role`
   hides the role's inner sub-tags behind the include statement, so
   `--tags browser:configure` would skip the whole role. Static `import_role`
   exposes inner tags to `--tags` and `--list-tags`.

2. **Bootstrap tasks are tagged `always`.** Any task a sub-tag path depends on —
   OS-var loaders (`include_vars`), capability detection, derived-fact `set_fact`s —
   must carry `tags: [always]`, not the bare role tag. Otherwise an isolated
   sub-tag run skips the loader and fails on undefined `__<role>_*` vars.
   Feature work keeps `role` + sub-tag; only genuine setup is `always`.

```yaml
- name: Main | Load OS-specific variables
  ansible.builtin.include_vars: '{{ item }}'
  with_first_found: ...
  tags:
    - always        # bootstrap — needed by every sub-tag path
```

#### Role toggles

The role default in `defaults/main.yml` is the single source of truth for
`<role>_enabled`: core desktop roles default to `true`, application and
peripheral roles to `false`. Inventory `group_vars` hold overrides only.

- **`import_role` reads `when: <role>_enabled | bool`** — no `default()`. The
  condition is attached to every task of the imported role and evaluated with
  the role defaults in scope, so the toggle is always defined and a playbook
  `default()` would be dead code (`public: false` does not change this).
- **`include_role` mirrors the role default:** `when: <role>_enabled | default(<role default>) | bool`.
  The condition runs before the role loads, so the `default()` is needed there
  and must match the role default.

## Security

- Vault files (`vault.yml`) are never accessed — only `vault.yml.example` templates
- Use `{{ vault_* }}` variable references, never hardcode secrets
- See root `.claude/CLAUDE.md` for vault protection rules
