# marcstraube.desktop.terminal

Install terminal emulators (Ghostty, Alacritty, Kitty, Foot, Wezterm)

## Description

Install and configure terminal emulators across multiple Linux distributions.
Supports Ghostty, Alacritty, Kitty, Foot, Wezterm, Konsole, and GNOME Terminal.
Terminal availability varies by OS — unavailable terminals are reported via debug
messages. Optional per-terminal configuration deployment and Kitty image support.

## Requirements

- ansible-core >= 2.17
- No additional collections required

## Supported Platforms

| Platform                   | Notes |
|----------------------------|-------|
| Arch Linux                 |       |
| Debian Trixie              |       |
| EL 9 (Rocky, Alma, RHEL)   |       |
| EL 10 (Rocky, Alma, RHEL)  |       |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable           | Default | Description              |
|--------------------|---------|--------------------------|
| `terminal_enabled` | `true`  | Enable the terminal role |

### Terminal Emulators

| Variable             | Default                               | Description                                              |
|----------------------|---------------------------------------|----------------------------------------------------------|
| `terminal_emulators` | `['ghostty']`                         | List of terminal emulators to install                    |
| `terminal_default`   | `'{{ terminal_emulators \| first }}'` | Default `$TERMINAL` (empty disables env file deployment) |

When `terminal_default` is non-empty, the role writes
`/etc/environment.d/terminal.conf` containing `TERMINAL=<value>`,
exposing it as a system-wide environment variable for desktop sessions.
Set `terminal_default: ''` to skip the env file (and remove it on
existing systems).

Per-terminal configuration (fonts, themes, custom configs) is left to
the user's dotfiles. Manage these via `~/.config/<terminal>/` directly.

### Kitty Options

| Variable                        | Default | Description                       |
|---------------------------------|---------|-----------------------------------|
| `terminal_kitty_images_enabled` | `true`  | Enable Kitty image support (icat) |

## Tags

| Tag                  | Scope                                    |
|----------------------|------------------------------------------|
| `terminal`           | All role tasks                           |
| `terminal:install`   | Package installation                     |
| `terminal:configure` | Default `$TERMINAL` env file in /etc/env |

## Example Playbook

```yaml
- name: Include terminal role
  ansible.builtin.include_role:
    name: marcstraube.desktop.terminal
  tags: [terminal]
  when: terminal_enabled | default(true) | bool
```

## Testing

```bash
cd roles/terminal
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## References

- [Ghostty](https://ghostty.org/) — Fast, native, GPU-accelerated terminal emulator
- [Alacritty](https://alacritty.org/) — Cross-platform GPU-accelerated terminal emulator
- [Kitty](https://sw.kovidgoyal.net/kitty/) — Fast, feature-rich, GPU-based terminal with image support
- [Foot](https://codeberg.org/dnkl/foot) — Fast, lightweight, minimalist Wayland terminal emulator
- [WezTerm](https://wezterm.org/) — GPU-accelerated cross-platform terminal emulator and multiplexer
- [systemd.environment-generators(7)](https://www.freedesktop.org/software/systemd/man/latest/environment.d.html) — `/etc/environment.d/` reference

## License

MIT

## Author

Marc Straube
