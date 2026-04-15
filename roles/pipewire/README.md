# marcstraube.desktop.pipewire

Install and configure PipeWire audio server.

## Description

Installs and configures PipeWire as the system audio server, replacing PulseAudio.
Supports PulseAudio and JACK compatibility layers, ALSA integration, Bluetooth audio,
real-time scheduling, and custom audio configuration. Manages PipeWire as user-scope
systemd services.

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

| Variable                   | Default | Description                        |
|----------------------------|---------|------------------------------------|
| `pipewire_enabled`         | `true`  | Enable the pipewire role           |
| `pipewire_service_enabled` | `true`  | Enable and start PipeWire services |

### Components

| Variable                   | Default         | Description                                                     |
|----------------------------|-----------------|-----------------------------------------------------------------|
| `pipewire_audio_enabled`   | `true`          | Install PipeWire audio support                                  |
| `pipewire_session_manager` | `'wireplumber'` | Session manager (wireplumber or pipewire-media-session)         |

### Compatibility Layers

| Variable                      | Default | Description                   |
|-------------------------------|---------|-------------------------------|
| `pipewire_pulseaudio_enabled` | `true`  | Enable PulseAudio replacement |
| `pipewire_alsa_enabled`       | `true`  | Enable ALSA integration       |
| `pipewire_jack_enabled`       | `false` | Enable JACK replacement       |

### Bluetooth

| Variable                     | Default | Description                    |
|------------------------------|---------|--------------------------------|
| `pipewire_bluetooth_enabled` | `true`  | Enable Bluetooth audio support |

### Network Audio

| Variable                    | Default | Description                         |
|-----------------------------|---------|-------------------------------------|
| `pipewire_zeroconf_enabled` | `false` | Enable Zeroconf/Avahi network audio |

### 32-Bit Support

| Variable                 | Default | Description                            |
|--------------------------|---------|----------------------------------------|
| `pipewire_32bit_enabled` | `false` | Install 32-bit libraries (Steam, Wine) |

### Real-Time Scheduling

| Variable                    | Default | Description                                                  |
|-----------------------------|---------|--------------------------------------------------------------|
| `pipewire_realtime_enabled` | `true`  | Enable real-time scheduling                                  |
| `pipewire_realtime_users`   | `[]`    | Users to add to realtime group (empty = all from users_list) |

### GUI Tools

| Variable                  | Default          | Description                              |
|---------------------------|------------------|------------------------------------------|
| `pipewire_volume_control` | `'pavucontrol'`  | Volume control GUI (pavucontrol, none)   |
| `pipewire_patchbay`       | `'none'`         | Patchbay editor (helvum, qpwgraph, none) |

### Configuration

| Variable                         | Default | Description                     |
|----------------------------------|---------|---------------------------------|
| `pipewire_custom_config_enabled` | `false` | Deploy custom PipeWire config   |
| `pipewire_sample_rate`           | `48000` | Default sample rate             |
| `pipewire_quantum`               | `1024`  | Default buffer size (quantum)   |
| `pipewire_min_quantum`           | `32`    | Minimum quantum                 |
| `pipewire_max_quantum`           | `2048`  | Maximum quantum                 |

### Cleanup

| Variable                             | Default | Description                            |
|--------------------------------------|---------|----------------------------------------|
| `pipewire_remove_pulseaudio_enabled` | `true`  | Remove conflicting PulseAudio packages |

## Tags

| Tag                  | Scope                |
|----------------------|----------------------|
| `pipewire`           | All role tasks       |
| `pipewire:install`   | Package installation |
| `pipewire:configure` | Configuration        |
| `pipewire:service`   | Service management   |
| `pipewire:cleanup`   | PulseAudio removal   |
| `pipewire:realtime`  | Real-time scheduling |

## Example Playbook

```yaml
- name: Include pipewire role
  ansible.builtin.include_role:
    name: marcstraube.desktop.pipewire
  tags:
    - pipewire
  when: pipewire_enabled | default(true) | bool
```

## Testing

```bash
cd roles/pipewire
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
