# marcstraube.desktop.desktop_environment

Install and configure desktop environments.

## Description

Installs and configures one or more desktop environments from a selectable list:
Hyprland, Sway, i3, KDE Plasma, GNOME, XFCE, LXDE, and LXQt. Supports optional
Wayland utilities integration, theme installation, and common desktop applications.

## Requirements

- ansible-core >= 2.17
- `community.general` collection
- `kewlfft.aur` collection (Arch Linux AUR packages)
- `marcstraube.desktop.wayland_utils` role (optional, for Wayland DEs)

## Supported Platforms

| Platform                  | Notes                                             |
|---------------------------|---------------------------------------------------|
| Arch Linux                | Full support including AUR                        |
| Debian Trixie             | Limited Hyprland extras                           |
| EL 9 (Rocky, Alma, RHEL)  | EPEL — limited Hyprland extras                    |
| EL 10 (Rocky, Alma, RHEL) | EPEL — limited Hyprland extras; XFCE not packaged |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                      | Default | Description                         |
|-------------------------------|---------|-------------------------------------|
| `desktop_environment_enabled` | `true`  | Enable the desktop_environment role |

### Users

| Variable                    | Default | Description                                |
|-----------------------------|---------|--------------------------------------------|
| `desktop_environment_users` | `[]`    | List of usernames for user-scoped services |

### Desktop Environments

| Variable                   | Default        | Description                     |
|----------------------------|----------------|---------------------------------|
| `desktop_environment_list` | `['hyprland']` | Desktop environments to install |

### Wayland Utilities

| Variable                                            | Default | Description                                |
|-----------------------------------------------------|---------|--------------------------------------------|
| `desktop_environment_wayland_utils_enabled`         | `true`  | Auto-install wayland_utils for Wayland DEs |
| `desktop_environment_wayland_utils_config`          | `{}`    | Per-DE wayland_utils overrides             |
| `desktop_environment_wayland_utils_hyprland_config` | dict    | Hyprland-specific wayland_utils settings   |

### Hyprland Options

| Variable                                             | Default | Description                                |
|------------------------------------------------------|---------|--------------------------------------------|
| `desktop_environment_hyprland_hypridle_enabled`      | `true`  | Install hypridle idle daemon               |
| `desktop_environment_hyprland_hyprlock_enabled`      | `true`  | Install hyprlock lock screen               |
| `desktop_environment_hyprland_hyprpaper_enabled`     | `true`  | Install hyprpaper wallpaper daemon         |
| `desktop_environment_hyprland_hyprpicker_enabled`    | `true`  | Install hyprpicker color picker            |
| `desktop_environment_hyprland_hyprcursor_enabled`    | `true`  | Install hyprcursor cursor theme engine     |
| `desktop_environment_hyprland_hyprshot_enabled`      | `true`  | Install hyprshot screenshot tool           |
| `desktop_environment_hyprland_hyprsunset_enabled`    | `true`  | Install hyprsunset blue-light filter       |
| `desktop_environment_hyprland_hyprlauncher_enabled`  | `true`  | Install hyprlauncher app launcher          |
| `desktop_environment_hyprland_hyprpwcenter_enabled`  | `true`  | Install hyprpwcenter password center       |
| `desktop_environment_hyprland_hyprqt6engine_enabled` | `false` | Install hyprqt6engine Qt6 theme (AUR)      |
| `desktop_environment_hyprland_hyprshutdown_enabled`  | `true`  | Install hyprshutdown shutdown dialog (AUR) |
| `desktop_environment_hyprland_portal_enabled`        | `true`  | Install xdg-desktop-portal-hyprland        |
| `desktop_environment_hyprland_polkit_enabled`        | `true`  | Install hyprpolkitagent                    |
| `desktop_environment_hyprland_uwsm_enabled`          | `false` | Enable Universal Wayland Session Manager   |
| `desktop_environment_hyprland_uwsm_services`         | list    | uwsm services to configure                 |
| `desktop_environment_hyprland_shader_enabled`        | `false` | Install hyprshade screen shader (AUR)      |

### Sway Options

| Variable                                  | Default | Description                      |
|-------------------------------------------|---------|----------------------------------|
| `desktop_environment_sway_extras_enabled` | `true`  | Install swaylock/swayidle/swaybg |
| `desktop_environment_sway_portal_enabled` | `true`  | Install xdg-desktop-portal-wlr   |

### i3 Options

| Variable                               | Default      | Description                            |
|----------------------------------------|--------------|----------------------------------------|
| `desktop_environment_i3_status`        | `'i3status'` | Status bar (i3status/i3blocks/polybar) |
| `desktop_environment_i3_dmenu_enabled` | `true`       | Install dmenu                          |
| `desktop_environment_i3_picom_enabled` | `true`       | Install picom compositor               |

### KDE Options

| Variable                               | Default | Description              |
|----------------------------------------|---------|--------------------------|
| `desktop_environment_kde_full_enabled` | `false` | Install full plasma-meta |
| `desktop_environment_kde_apps`         | `[]`    | Additional KDE apps      |

### GNOME Options

| Variable                                   | Default | Description               |
|--------------------------------------------|---------|---------------------------|
| `desktop_environment_gnome_full_enabled`   | `false` | Install full gnome group  |
| `desktop_environment_gnome_extras_enabled` | `false` | Install gnome-extra group |
| `desktop_environment_gnome_tweaks_enabled` | `true`  | Install gnome-tweaks      |

### XFCE Options

| Variable                                       | Default | Description                     |
|------------------------------------------------|---------|---------------------------------|
| `desktop_environment_xfce_goodies_enabled`     | `true`  | Install xfce4-goodies group     |
| `desktop_environment_xfce_whiskermenu_enabled` | `true`  | Install modern application menu |

### LXDE Options

| Variable                                | Default | Description             |
|-----------------------------------------|---------|-------------------------|
| `desktop_environment_lxde_full_enabled` | `true`  | Install full lxde group |

### LXQt Options

| Variable                           | Default          | Description              |
|------------------------------------|------------------|--------------------------|
| `desktop_environment_lxqt_variant` | `'full'`         | Variant: minimal or full |
| `desktop_environment_lxqt_icons`   | `'breeze-icons'` | Icon theme               |

### Common Options

| Variable                                      | Default  | Description                     |
|-----------------------------------------------|----------|---------------------------------|
| `desktop_environment_file_manager`            | `'none'` | File manager for standalone WMs |
| `desktop_environment_archive_manager_enabled` | `false`  | Install archive manager         |
| `desktop_environment_calculator_enabled`      | `false`  | Install calculator              |
| `desktop_environment_text_editor`             | `'none'` | Simple text editor              |

### Theme Options

| Variable                            | Default | Description              |
|-------------------------------------|---------|--------------------------|
| `desktop_environment_cursor_themes` | `[]`    | Cursor themes to install |
| `desktop_environment_icon_themes`   | `[]`    | Icon themes to install   |

## Tags

| Tag                           | Scope               |
|-------------------------------|---------------------|
| `desktop-environment`         | All role tasks      |
| `desktop-environment:wayland` | Wayland utilities   |
| `desktop-environment:common`  | Common applications |
| `desktop-environment:themes`  | Theme installation  |

## Example Playbook

```yaml
- name: Include desktop_environment role
  ansible.builtin.include_role:
    name: marcstraube.desktop.desktop_environment
  tags:
    - desktop-environment
  when: desktop_environment_enabled | default(true) | bool
```

### Hyprland with Extras

```yaml
- name: Include desktop_environment role
  ansible.builtin.include_role:
    name: marcstraube.desktop.desktop_environment
  vars:
    desktop_environment_list:
      - 'hyprland'
    desktop_environment_hyprland_uwsm_enabled: true
    desktop_environment_file_manager: 'thunar'
    desktop_environment_cursor_themes:
      - bibata
  tags:
    - desktop-environment
  when: desktop_environment_enabled | default(true) | bool
```

## Testing

```bash
cd roles/desktop_environment
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## References

- [Hyprland](https://hypr.land/) — Dynamic tiling Wayland compositor
- [Sway](https://swaywm.org/) — i3-compatible Wayland compositor
- [i3](https://i3wm.org/) — Tiling window manager (X11)
- [KDE Plasma](https://kde.org/plasma-desktop/) — Full-featured Qt desktop environment
- [GNOME](https://www.gnome.org/) — Modern GTK desktop environment
- [XFCE](https://xfce.org/) — Lightweight GTK desktop environment
- [LXDE](https://lxde.org/) — Lightweight X11 desktop environment
- [LXQt](https://lxqt-project.org/) — Lightweight Qt desktop environment
- [UWSM](https://github.com/Vladimir-csp/uwsm) — Universal Wayland Session Manager
- [hyprland-qt-support](https://github.com/hyprwm/hyprland-qt-support) and the Hypr* ecosystem (hypridle, hyprlock, hyprpaper, hyprpicker, hyprshot, hyprsunset, hyprlauncher) — Companion utilities to Hyprland

## License

MIT

## Author

Marc Straube
