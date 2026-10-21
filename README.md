# Ansible Collection: marcstraube.desktop

[![CI](https://github.com/marcstraube/ansible-collection-desktop/workflows/CI/badge.svg)](https://github.com/marcstraube/ansible-collection-desktop/actions)
[![Release](https://img.shields.io/github/v/release/marcstraube/ansible-collection-desktop?display_name=tag&sort=semver)](https://github.com/marcstraube/ansible-collection-desktop/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-PayPal-blue.svg)](https://paypal.me/marcstraube)

## Description

Desktop workstation roles for Arch Linux, Debian Trixie, and EL 9/10.
Roles covering desktop environments, display managers, browsers,
development tools, multimedia, office, and productivity applications.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Supported Platforms

- Arch Linux (primary)
- Debian Trixie (13)
- EL 9 (Rocky, Alma, RHEL)
- EL 10 (Rocky, Alma, RHEL)

## Requirements

- ansible-core >= 2.19
- [marcstraube.common](https://github.com/marcstraube/ansible-collection-common) >= 3.0.0

## Included Roles

### Desktop Environment & Display

| Role                    | Description                                     |
| ----------------------- | ----------------------------------------------- |
| **desktop_environment** | Hyprland, Sway, GNOME, KDE, i3, XFCE, LXDE/LXQt |
| **display_manager**     | greetd, GDM, SDDM, LightDM with greeter config  |
| **wayland_utils**       | Wayland clipboard, screenshot, and screen tools |
| **plymouth**            | Boot splash screen                              |

### Core Applications

| Role          | Description                                        |
| ------------- | -------------------------------------------------- |
| **terminal**  | Ghostty, Alacritty, Kitty, Foot                    |
| **browser**   | Firefox, LibreWolf, Chromium, Brave with policies  |
| **office**    | LibreOffice, Thunderbird, Obsidian, language packs |
| **keepassxc** | KeePassXC password manager, browser/secret service |

### Audio & Hardware

| Role          | Description                                   |
| ------------- | --------------------------------------------- |
| **pipewire**  | PipeWire audio server with low-latency config |
| **bluetooth** | BlueZ configuration, security, MAC privacy    |
| **elgato**    | Elgato hardware support                       |
| **tuxedo**    | TUXEDO hardware support                       |

### User Environment

| Role              | Description                                         |
| ----------------- | --------------------------------------------------- |
| **xdg_user_dirs** | XDG user dirs with locale, skip and custom entries  |

### Development & AI

| Role            | Description                                |
| --------------- | ------------------------------------------ |
| **development** | IDEs, database/API tools, homebrew SDKs    |
| **ai**          | Claude Code, Ollama, Antigravity, API keys |

### Multimedia & Graphics

| Role              | Description           |
| ----------------- | --------------------- |
| **multimedia**    | Multimedia tools      |
| **graphics_apps** | Graphics applications |
| **imaging**       | Imaging tools         |

### Productivity

| Role              | Description           |
| ----------------- | --------------------- |
| **filemanagers**  | File managers         |
| **communication** | Communication tools   |
| **downloads**     | Download tools        |
| **remote_access** | Remote access tools   |
| **security_apps** | Security applications |
| **system_apps**   | System utilities      |

### Gaming & Hobby

| Role                | Description                             |
| ------------------- | --------------------------------------- |
| **gaming**          | Gaming platforms, emulators, launchers  |
| **virtual_reality** | VR streaming to standalone headsets     |
| **wine**            | Wine Windows compatibility layer        |
| **cad**             | CAD applications                        |

## Installation

### From Ansible Galaxy

```bash
ansible-galaxy collection install marcstraube.desktop
```

### From Git

```bash
ansible-galaxy collection install git+https://github.com/marcstraube/ansible-collection-desktop.git,main
```

### Requirements File

```yaml
# requirements.yml
collections:
  - name: marcstraube.desktop
    version: ">=1.0.0"
```

## Usage

### Playbook

`marcstraube.desktop.workstation` runs the desktop roles on the
`workstations` group (desktops and laptops). Core desktop roles default to
enabled, application and peripheral roles are opt-in; set
`<role>_enabled` and the role variables in the inventory. Run
`marcstraube.common.base_system` first for the base system:

```bash
ansible-playbook marcstraube.common.base_system -i inventory/
ansible-playbook marcstraube.desktop.workstation -i inventory/
```

Or combine both in one playbook:

```yaml
# site.yml
- name: Base system
  ansible.builtin.import_playbook: marcstraube.common.base_system

- name: Workstations
  ansible.builtin.import_playbook: marcstraube.desktop.workstation
```

`playbooks/tasks/workstation.yml` imports every role of the collection with
`import_role` and the role toggles, so a play can import that task file
instead of listing the roles itself.

### Individual roles

All roles use `include_role` with boolean toggles:

```yaml
- name: Configure desktop workstation
  hosts: workstations
  become: true

  tasks:
    - name: Include desktop environment role
      ansible.builtin.include_role:
        name: marcstraube.desktop.desktop_environment
      when: desktop_environment_enabled | default(true) | bool

    - name: Include browser role
      ansible.builtin.include_role:
        name: marcstraube.desktop.browser
      when: browser_enabled | default(true) | bool
```

Each role documents its variables in `defaults/main.yml` and `roles/<role>/README.md`.

## Testing

Roles are tested with Molecule using Podman containers across supported platforms.

```bash
cd roles/<role>
molecule test
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.
Pull requests target the `develop` branch; `main` holds the released state.

## License

MIT

## Author

Marc Straube (<email@marcstraube.de>)
