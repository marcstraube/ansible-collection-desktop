# marcstraube.desktop.multimedia

Install multimedia applications for audio and video.

## Description

This role installs multimedia applications organized by category: video players,
audio editors, video editors, media converters, screen recording tools, music
players, and audio visualization. Each application is individually toggleable.

- Install VLC, MPV, Audacity, Ardour, Kdenlive, OpenShot, HandBrake, Peek,
  OBS Studio, SimpleScreenRecorder, Rhythmbox, and Cava
- Install FFMultiConverter from AUR on Arch Linux
- Skip unavailable packages per platform (Ardour, HandBrake, FFMultiConverter,
  SimpleScreenRecorder not in EL repos)

## Requirements

- ansible-core >= 2.17
- `kewlfft.aur` collection (Arch Linux AUR packages)

## Supported Platforms

| Platform                  | Notes                                                                 |
|---------------------------|-----------------------------------------------------------------------|
| Arch Linux                |                                                                       |
| Debian Trixie             |                                                                       |
| EL 9 (Rocky, Alma, RHEL)  | Ardour, HandBrake, FFMultiConverter, SimpleScreenRecorder unavailable |
| EL 10 (Rocky, Alma, RHEL) | Ardour, HandBrake, FFMultiConverter, SimpleScreenRecorder unavailable |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable             | Default | Description                |
|----------------------|---------|----------------------------|
| `multimedia_enabled` | `true`  | Enable the multimedia role |

### Video Players

| Variable                 | Default | Description             |
|--------------------------|---------|-------------------------|
| `multimedia_vlc_enabled` | `true`  | Enable VLC media player |
| `multimedia_mpv_enabled` | `false` | Enable MPV media player |

### Audio Editors

| Variable                      | Default | Description                             |
|-------------------------------|---------|-----------------------------------------|
| `multimedia_audacity_enabled` | `true`  | Enable Audacity audio editor            |
| `multimedia_ardour_enabled`   | `false` | Enable Ardour digital audio workstation |

### Video Editors

| Variable                      | Default | Description                  |
|-------------------------------|---------|------------------------------|
| `multimedia_kdenlive_enabled` | `false` | Enable Kdenlive video editor |
| `multimedia_openshot_enabled` | `false` | Enable OpenShot video editor |

### Converters

| Variable                              | Default | Description                             |
|---------------------------------------|---------|-----------------------------------------|
| `multimedia_ffmulticonverter_enabled` | `true`  | Enable FFMultiConverter media converter |
| `multimedia_handbrake_enabled`        | `false` | Enable HandBrake video transcoder       |

### Screen Recording

| Variable                                  | Default | Description                           |
|-------------------------------------------|---------|---------------------------------------|
| `multimedia_peek_enabled`                 | `true`  | Enable Peek animated GIF recorder     |
| `multimedia_obs_enabled`                  | `false` | Enable OBS Studio streaming/recording |
| `multimedia_simplescreenrecorder_enabled` | `false` | Enable SimpleScreenRecorder           |

### Music Players

| Variable                       | Default | Description                         |
|--------------------------------|---------|-------------------------------------|
| `multimedia_rhythmbox_enabled` | `false` | Enable Rhythmbox GNOME music player |

### Audio Visualization

| Variable                  | Default | Description                          |
|---------------------------|---------|--------------------------------------|
| `multimedia_cava_enabled` | `false` | Enable Cava console audio visualizer |

## Tags

| Tag                  | Scope                |
|----------------------|----------------------|
| `multimedia`         | All tasks            |
| `multimedia:install` | Package installation |

## Example Playbook

```yaml
- name: Include multimedia role
  ansible.builtin.include_role:
    name: marcstraube.desktop.multimedia
  tags:
    - multimedia
  when: multimedia_enabled | default(true) | bool
```

## Testing

```bash
cd roles/multimedia
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
