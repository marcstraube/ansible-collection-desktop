# marcstraube.desktop.pipewire

Install and configure PipeWire audio server.

## Description

Installs and configures PipeWire as the system audio server, replacing PulseAudio.
Supports PulseAudio and JACK compatibility layers, ALSA integration, Bluetooth audio,
real-time scheduling, and custom audio configuration. Installs ALSA firmware and
utilities on request and deploys ALSA Card Profile (ACP) files, udev rules, and
bundled quirks for specific sound cards. Manages PipeWire as user-scope systemd
services.

## Requirements

- ansible-core >= 2.19
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

### ALSA Support

| Variable                         | Default | Description                                                        |
|----------------------------------|---------|--------------------------------------------------------------------|
| `pipewire_alsa_firmware_enabled` | `false` | Install ALSA firmware for sound cards with an onboard DSP          |
| `pipewire_alsa_utils_enabled`    | `false` | Install ALSA utilities (`alsactl`, `alsamixer`, `amixer`, `aplay`) |

`alsa-firmware` is available on Arch Linux and EL. Debian has no equivalent
package (`firmware-misc-nonfree` lacks `ctefx-desktop.bin`), so the toggle has
no effect there.

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

### ALSA Card Profiles

| Variable                  | Default | Description                                                             |
|---------------------------|---------|-------------------------------------------------------------------------|
| `pipewire_acp_quirks`     | `[]`    | Bundled quirks for specific sound cards (see [ACP Quirks](#acp-quirks)) |
| `pipewire_acp_files`      | `[]`    | Custom ACP files from `{{ inventory_dir }}/files/acp/`                  |
| `pipewire_acp_udev_rules` | `[]`    | udev rules that select a profile set for a specific sound card          |

`pipewire_acp_files` entries:

| Key    | Required | Description                                                               |
|--------|----------|---------------------------------------------------------------------------|
| `src`  | yes      | File below `{{ inventory_dir }}/files/acp/`, deployed under its file name |
| `type` | yes      | Target directory: `paths` or `profile-sets`                               |

`pipewire_acp_udev_rules` entries:

| Key           | Required | Description                                         |
|---------------|----------|-----------------------------------------------------|
| `name`        | yes      | Comment above the rule                              |
| `match`       | yes      | udev match keys of the sound card                   |
| `profile_set` | yes      | Profile set file name to select (`ACP_PROFILE_SET`) |

```yaml
pipewire_acp_files:
  - src: 'my-card-analog-output.conf'
    type: 'paths'
  - src: 'my-card.conf'
    type: 'profile-sets'

pipewire_acp_udev_rules:
  - name: 'My sound card'
    match: 'ATTRS{subsystem_vendor}=="0x1234", ATTRS{subsystem_device}=="0x5678"'
    profile_set: 'my-card.conf'
```

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
| `pipewire:acp`       | ALSA Card Profiles   |
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

## Notes

### ALSA Card Profiles

PipeWire looks up every ACP path and profile-set file in
`~/.config/alsa-card-profile/mixer/`, then `/etc/alsa-card-profile/mixer/`, then
the packaged `/usr/share/alsa-card-profile/mixer/`. The role deploys to
`/etc/alsa-card-profile/mixer/`, so the files apply to all users. A file there
with the name of a packaged file replaces it for every sound card; use own file
names and a profile set selected by a udev rule to limit a change to one card.

udev rules go to `/etc/udev/rules.d/91-pipewire-acp.rules`, which runs after the
packaged `90-pipewire-alsa.rules`. After a change the role reloads the udev
rules, triggers the sound devices, and restarts the PipeWire user services of
`pipewire_users`; other sessions pick up the change at their next login. The
rules file is deployed while at least one quirk or udev rule is configured.

### ACP Quirks

Quirks are opt-in. A quirk renames the card's ports, so WirePlumber does not
restore the previously stored route for that card once.

| Quirk               | Card                                         | Match (PCI subsystem) |
|---------------------|----------------------------------------------|-----------------------|
| `creative_ae5_plus` | Creative Sound BlasterX AE-5 Plus (CA0132)   | `1102:0191`           |

`creative_ae5_plus`:

- The headphone path keeps the `Front` element in the volume chain instead of
  muting it. The CA0132 feeds the headphone jack from the Front DAC, so the
  packaged path silences the headphones
  ([pipewire/pipewire#5102](https://gitlab.freedesktop.org/pipewire/pipewire/-/issues/5102)).
- Every output path sets `Output Select` to its own jack: line-out paths select
  `Speakers`, the headphone path selects `Headphone`. The packaged files offer
  both jacks on every path.
- The profile set includes the packaged `default.conf` and only replaces the
  output paths of the analog mappings.
- The card's DSP needs `ctefx-desktop.bin`: set
  `pipewire_alsa_firmware_enabled: true`. On Debian the firmware is not
  packaged and the card stays silent.

The quirk path files are based on `alsa-card-profiles` 1.6.9, which matches the
files in PipeWire 1.4.2 (Debian Trixie) and 1.4.11 (EL 9/10). They keep the
LGPL-2.1-or-later license header of the PulseAudio originals.

## License

MIT

## Author

Marc Straube
