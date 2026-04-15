# marcstraube.desktop.display_manager

Install and configure display managers.

## Description

Installs and configures display managers including SDDM, GDM, LightDM, and greetd.
Supports autologin, greeter selection, and compositor configuration for graphical
greeters (gtkgreet, regreet) running under Hyprland, Sway, or Cage.

## Requirements

- ansible-core >= 2.17

## Supported Platforms

| Platform                  | Notes |
|---------------------------|-------|
| Arch Linux                |       |
| Debian Trixie             |       |
| EL 9 (Rocky, Alma, RHEL)  |       |
| EL 10 (Rocky, Alma, RHEL) |       |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                          | Default | Description                                  |
|-----------------------------------|---------|----------------------------------------------|
| `display_manager_enabled`         | `true`  | Enable the display_manager role              |
| `display_manager_service_enabled` | `true`  | Enable and start the display manager service |

### Display Manager Selection

| Variable               | Default | Description                                 |
|------------------------|---------|---------------------------------------------|
| `display_manager_name` | `sddm`  | Display manager: sddm, gdm, lightdm, greetd |

### SDDM Options

| Variable                                | Default | Description                         |
|-----------------------------------------|---------|-------------------------------------|
| `display_manager_sddm_theme`            | `''`    | SDDM theme (empty = default breeze) |
| `display_manager_sddm_virtual_keyboard` | `false` | Enable virtual keyboard             |

### GDM Options

| Variable                      | Default | Description                       |
|-------------------------------|---------|-----------------------------------|
| `display_manager_gdm_wayland` | `true`  | Wayland session (false = use X11) |

### LightDM Options

| Variable                          | Default | Description                     |
|-----------------------------------|---------|---------------------------------|
| `display_manager_lightdm_greeter` | `gtk`   | Greeter: gtk, slick             |
| `display_manager_lightdm_theme`   | `''`    | Greeter theme (empty = default) |

### greetd Options

| Variable                                    | Default    | Description                                             |
|---------------------------------------------|------------|---------------------------------------------------------|
| `display_manager_greetd_greeter`            | `agreety`  | Greeter: agreety, tuigreet, gtkgreet, regreet           |
| `display_manager_greetd_greeter_compositor` | `''`       | Compositor for graphical greeters: hyprland, sway, cage |
| `display_manager_greetd_greeter_command`    | `''`       | Greeter command override (auto-generated if empty)      |
| `display_manager_greetd_default_session`    | `Hyprland` | Default session for greeter                             |
| `display_manager_greetd_vt`                 | `1`        | VT to run on                                            |
| `display_manager_greetd_keyboard_layout`    | `''`       | Keyboard layout (XKB format, empty = system default)    |
| `display_manager_greetd_keyboard_variant`   | `''`       | Keyboard variant                                        |

### Autologin

| Variable                            | Default | Description                         |
|-------------------------------------|---------|-------------------------------------|
| `display_manager_autologin_enabled` | `false` | Enable autologin                    |
| `display_manager_autologin_user`    | `''`    | Autologin user                      |
| `display_manager_autologin_session` | `''`    | Autologin session (empty = default) |

### NumLock

| Variable                  | Default | Description               |
|---------------------------|---------|---------------------------|
| `display_manager_numlock` | `false` | Enable NumLock on startup |

## Tags

| Tag                         | Scope                |
|-----------------------------|----------------------|
| `display-manager`           | All role tasks       |
| `display-manager:install`   | Package installation |
| `display-manager:configure` | Configuration        |
| `display-manager:service`   | Service management   |

## Example Playbook

```yaml
- name: Include display_manager role
  ansible.builtin.include_role:
    name: marcstraube.desktop.display_manager
  tags:
    - display-manager
  when: display_manager_enabled | default(true) | bool
```

### greetd with gtkgreet on Hyprland

```yaml
- name: Include display_manager role
  ansible.builtin.include_role:
    name: marcstraube.desktop.display_manager
  vars:
    display_manager_name: 'greetd'
    display_manager_greetd_greeter: 'gtkgreet'
    display_manager_greetd_greeter_compositor: 'hyprland'
  tags:
    - display-manager
  when: display_manager_enabled | default(true) | bool
```

## Testing

```bash
cd roles/display_manager
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
