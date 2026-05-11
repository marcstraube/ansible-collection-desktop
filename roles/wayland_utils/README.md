# wayland_utils

Install common Wayland utilities including clipboard tools, screenshot/recording
tools, notification daemons, application launchers, status bars, idle/lock
managers, wallpaper tools, display management, XDG portals, and miscellaneous
input/event utilities.

EPEL is X11-focused, so on Rocky Linux only a small subset of Wayland
tooling is packaged. Most things (grim, slurp, mako, dunst, wofi, waybar,
swayidle, swaylock, hyprland stack, …) are not in EPEL and silently
skipped. Use Arch Linux or Debian for full Wayland coverage.

## Requirements

None.

## Supported Platforms

| Platform                   | Notes                                                                                |
|----------------------------|--------------------------------------------------------------------------------------|
| Arch Linux                 | Full coverage                                                                        |
| Debian Trixie              | Full coverage                                                                        |
| EL 9 (Rocky, Alma, RHEL)   | EPEL — only wl-clipboard, XDG portals, brightnessctl, playerctl, obs-studio          |
| EL 10 (Rocky, Alma, RHEL)  | EPEL — only wl-clipboard and XDG portals                                             |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                | Default | Description                   |
|-------------------------|---------|-------------------------------|
| `wayland_utils_enabled` | `true`  | Enable the wayland_utils role |

### Clipboard

| Variable                          | Default | Description                                 |
|-----------------------------------|---------|---------------------------------------------|
| `wayland_utils_clipboard_enabled` | `true`  | Enable wl-clipboard (wl-copy, wl-paste)     |
| `wayland_utils_cliphist_enabled`  | `true`  | Enable cliphist (clipboard history manager) |

### Screenshots

| Variable                       | Default | Description                           |
|--------------------------------|---------|---------------------------------------|
| `wayland_utils_grim_enabled`   | `true`  | Enable grim (screenshot tool)         |
| `wayland_utils_slurp_enabled`  | `true`  | Enable slurp (region selection)       |
| `wayland_utils_swappy_enabled` | `true`  | Enable swappy (screenshot annotation) |

### Screen Recording

| Variable                          | Default | Description                                           |
|-----------------------------------|---------|-------------------------------------------------------|
| `wayland_utils_recorder_enabled`  | `false` | Enable wf-recorder (screen recorder)                  |
| `wayland_utils_screenrec_enabled` | `false` | Enable wl-screenrec (GPU-accelerated screen recorder) |
| `wayland_utils_obs_enabled`       | `false` | Enable OBS Studio (streaming/recording)               |

### Notifications

| Variable                      | Default  | Description                                   |
|-------------------------------|----------|-----------------------------------------------|
| `wayland_utils_notifications` | `'none'` | Notification daemon: mako, dunst, fnott, none |

### Application Launcher

| Variable                 | Default  | Description                                              |
|--------------------------|----------|----------------------------------------------------------|
| `wayland_utils_launcher` | `'none'` | Launcher: hyprlauncher, rofi, wofi, fuzzel, bemenu, none |

### Status Bar

| Variable            | Default  | Description                                 |
|---------------------|----------|---------------------------------------------|
| `wayland_utils_bar` | `'none'` | Status bar: waybar, hyprpanel, yambar, none |

### Idle and Lock

| Variable               | Default  | Description                                            |
|------------------------|----------|--------------------------------------------------------|
| `wayland_utils_idle`   | `'none'` | Idle daemon: swayidle, hypridle, none                  |
| `wayland_utils_locker` | `'none'` | Screen locker: swaylock, hyprlock, waylock, none       |

### Wallpaper

| Variable                  | Default  | Description                                                   |
|---------------------------|----------|---------------------------------------------------------------|
| `wayland_utils_wallpaper` | `'none'` | Wallpaper tool: swww, swaybg, hyprpaper, wpaperd, none        |

### Display Management

| Variable                             | Default | Description                              |
|--------------------------------------|---------|------------------------------------------|
| `wayland_utils_wlr_randr_enabled`    | `true`  | Enable wlr-randr (xrandr for wlroots)    |
| `wayland_utils_kanshi_enabled`       | `false` | Enable kanshi (autorandr for Wayland)    |
| `wayland_utils_nwg_displays_enabled` | `false` | Enable nwg-displays (GUI display config) |

### Portals

| Variable               | Default | Description                                                 |
|------------------------|---------|-------------------------------------------------------------|
| `wayland_utils_portal` | `'gtk'` | XDG Desktop Portal: gtk, wlr, hyprland, kde, gnome          |

### Shell Framework

| Variable                           | Default | Description                                       |
|------------------------------------|---------|---------------------------------------------------|
| `wayland_utils_quickshell_enabled` | `false` | Enable quickshell (Qt6/QML desktop shell toolkit) |

### Media and Brightness

| Variable                              | Default | Description                                            |
|---------------------------------------|---------|--------------------------------------------------------|
| `wayland_utils_brightnessctl_enabled` | `true`  | Enable brightnessctl (screen brightness control)       |
| `wayland_utils_playerctl_enabled`     | `true`  | Enable playerctl (media player control)                |

### Misc

| Variable                        | Default | Description                                        |
|---------------------------------|---------|----------------------------------------------------|
| `wayland_utils_wev_enabled`     | `true`  | Enable wev (wayland event viewer, like xev)        |
| `wayland_utils_wtype_enabled`   | `false` | Enable wtype (xdotool for Wayland)                 |
| `wayland_utils_ydotool_enabled` | `false` | Enable ydotool (input automation)                  |

## Tags

- `wayland` - All wayland_utils tasks
- `wayland:install` - Package installation only

## Example Playbook

```yaml
- hosts: workstations
  become: true

  tasks:
    - name: Include wayland_utils role
      ansible.builtin.include_role:
        name: marcstraube.desktop.wayland_utils
      tags:
        - wayland
      when: wayland_utils_enabled | default(true) | bool
```

## Testing

```bash
cd collections/ansible_collections/marcstraube/desktop/roles/wayland_utils
molecule test
```

## License

MIT

## Author

Marc Straube
