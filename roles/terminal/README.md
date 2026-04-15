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

| Variable             | Default                               | Description                              |
|----------------------|---------------------------------------|------------------------------------------|
| `terminal_emulators` | `['ghostty']`                         | List of terminal emulators to install    |
| `terminal_default`   | `'{{ terminal_emulators \| first }}'` | Default terminal (for $TERMINAL env var) |

### Ghostty Options

| Variable                          | Default | Description                  |
|-----------------------------------|---------|------------------------------|
| `terminal_ghostty_config_enabled` | `false` | Deploy custom Ghostty config |
| `terminal_ghostty_font_family`    | `''`    | Ghostty font family          |
| `terminal_ghostty_font_size`      | `12`    | Ghostty font size            |
| `terminal_ghostty_theme`          | `''`    | Ghostty theme                |

### Alacritty Options

| Variable                            | Default       | Description                    |
|-------------------------------------|---------------|--------------------------------|
| `terminal_alacritty_config_enabled` | `false`       | Deploy custom Alacritty config |
| `terminal_alacritty_font_family`    | `'monospace'` | Alacritty font family          |
| `terminal_alacritty_font_size`      | `12.0`        | Alacritty font size            |

### Kitty Options

| Variable                        | Default       | Description                       |
|---------------------------------|---------------|-----------------------------------|
| `terminal_kitty_config_enabled` | `false`       | Deploy custom Kitty config        |
| `terminal_kitty_font_family`    | `'monospace'` | Kitty font family                 |
| `terminal_kitty_font_size`      | `12`          | Kitty font size                   |
| `terminal_kitty_images_enabled` | `true`        | Enable Kitty image support (icat) |

### Foot Options

| Variable                       | Default               | Description               |
|--------------------------------|-----------------------|---------------------------|
| `terminal_foot_config_enabled` | `false`               | Deploy custom Foot config |
| `terminal_foot_font`           | `'monospace:size=12'` | Foot font                 |

### Wezterm Options

| Variable                          | Default | Description                  |
|-----------------------------------|---------|------------------------------|
| `terminal_wezterm_config_enabled` | `false` | Deploy custom Wezterm config |

## Tags

| Tag                | Scope                |
|--------------------|----------------------|
| `terminal`         | All role tasks       |
| `terminal:install` | Package installation |

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

## License

MIT

## Author

Marc Straube
