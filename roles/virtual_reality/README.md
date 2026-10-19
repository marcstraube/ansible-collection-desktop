# marcstraube.desktop.virtual_reality

Install VR streaming servers for standalone headsets.

## Description

Sets up PC VR streaming to standalone headsets such as the Meta Quest 2.
The PC renders, encodes the video and streams it to the headset over Wi-Fi
(or USB). Two streaming stacks are available:

| Stack | Backend                              | SteamVR titles      | Default   |
| ----- | ------------------------------------ | ------------------- | --------- |
| WiVRn | Monado (OpenXR), no SteamVR needed   | through xrizer      | enabled   |
| ALVR  | SteamVR                              | native              | disabled  |

WiVRn is the default: it is native OpenXR and does not depend on SteamVR,
which is fragile on Linux. SteamVR titles run on WiVRn through xrizer, an
OpenVR-to-OpenXR layer. While a headset is connected, the WiVRn server sets
the active OpenXR runtime and the OpenVR configuration on its own, so no
per-user configuration is deployed. ALVR stays available for SteamVR-centric
setups.

**Steam Link VR** is a third option that needs no component from this role:
it is the Steam client (`gaming_steam_enabled` in
`marcstraube.desktop.gaming`) plus SteamVR, which is a Steam app and not a
system package. Install the Steam Link app on the headset and open the
`steam-streaming` firewall service (see [Firewall](#firewall)).

WiVRn, ALVR and xrizer are only packaged for Arch Linux (AUR). On Debian and
EL the role installs nothing and shows a notice: install WiVRn from Flathub
(`io.github.wivrn.wivrn`) there, which bundles xrizer and OpenComposite.

## Requirements

- ansible-core >= 2.19
- `kewlfft.aur` collection (AUR packages on Arch Linux)
- `aur_builder` system user with passwordless sudo (Arch Linux only)
- Arch Linux + `virtual_reality_xrizer_enabled: true`: `multilib`
  repository enabled — set `pacman_multilib_enabled: true` in inventory
  and run the `marcstraube.common.package_management` role first (or use
  the `base-system` tag). xrizer ships a 32-bit build (`lib32-xrizer`) for
  32-bit SteamVR titles. The role asserts this precondition.
- WiVRn: Avahi running and allowed to publish user services — see
  [Service Discovery](#service-discovery)
- Hardware video encoding: VAAPI (AMD/Intel) or NVENC (NVIDIA), provided by
  the graphics stack

## Supported Platforms

| Platform                  | Notes                                          |
| ------------------------- | ---------------------------------------------- |
| Arch Linux                | Full support — AUR + official packages         |
| Debian Trixie             | Nothing installed; notice points to Flathub    |
| EL 9 (Rocky, Alma, RHEL)  | Nothing installed; notice points to Flathub    |
| EL 10 (Rocky, Alma, RHEL) | Nothing installed; notice points to Flathub    |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable                  | Default | Description                         |
| ------------------------- | ------- | ----------------------------------- |
| `virtual_reality_enabled` | `false` | Enable/disable virtual_reality role |

### Streaming Servers

| Variable                        | Default | Description                                                          |
| ------------------------------- | ------- | -------------------------------------------------------------------- |
| `virtual_reality_wivrn_enabled` | `true`  | WiVRn server and dashboard (`wivrn-server`, `wivrn-dashboard`, AUR)  |
| `virtual_reality_alvr_enabled`  | `false` | ALVR streaming server (`alvr-bin`, AUR); requires SteamVR            |

### Compatibility

| Variable                         | Default | Description                                                      |
| -------------------------------- | ------- | ---------------------------------------------------------------- |
| `virtual_reality_xrizer_enabled` | `true`  | xrizer OpenVR-to-OpenXR layer (`xrizer`, `lib32-xrizer`, AUR)    |

### Headset Access

| Variable                      | Default | Description                                                          |
| ----------------------------- | ------- | -------------------------------------------------------------------- |
| `virtual_reality_adb_enabled` | `true`  | ADB tools and udev rules (`android-tools`, `android-udev`) on Arch   |

ADB is needed to sideload a headset client that is not installed from the
headset's store, and for wired streaming over USB.

## Service Discovery

WiVRn announces itself on the local network via Avahi (mDNS/DNS-SD) as a
user service, so the headset finds the PC without entering an address. Use
`marcstraube.common.avahi` with its defaults — `avahi_service_enabled: true`
and `avahi_disable_user_service_publishing: false`.

## Firewall

The role does not manage firewall rules: they belong in the inventory, where
`marcstraube.common.firewalld` reconciles them, so a role-added rule would be
removed again by a purge. Open the services for the stacks in use:

| Stack      | Ports                   | firewalld service            |
| ---------- | ----------------------- | ---------------------------- |
| WiVRn      | 5353/udp (mDNS)         | `mdns` (shipped)             |
| WiVRn      | 9757/tcp, 9757/udp      | none — define one, see below |
| ALVR       | 9943-9944/tcp+udp       | `alvr` (shipped)             |
| Steam Link | Steam Remote Play ports | `steam-streaming` (shipped)  |

For WiVRn, a custom service is recommended, because the rule then shows up
by name instead of as bare ports:

```yaml
firewalld_custom_services:
  - name: 'wivrn'
    short: 'WiVRn'
    description: 'WiVRn VR streaming server'
    ports:
      - port: '9757'
        protocol: 'tcp'
      - port: '9757'
        protocol: 'udp'

firewalld_services:
  - ssh
  - mdns
  - wivrn
```

Alternatively, open the ports directly:

```yaml
firewalld_services:
  - ssh
  - mdns

firewalld_ports:
  - '9757/tcp'
  - '9757/udp'
```

## Tags

| Tag                       | Scope                |
| ------------------------- | -------------------- |
| `virtual-reality`         | All role tasks       |
| `virtual-reality:install` | Package installation |

## Example Playbook

```yaml
- name: Virtual Reality
  hosts: workstations
  tasks:
    - name: Include virtual_reality role
      ansible.builtin.include_role:
        name: marcstraube.desktop.virtual_reality
      tags: [virtual-reality]
      when: virtual_reality_enabled | default(false) | bool
```

## Testing

```bash
cd roles/virtual_reality
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10
- Arch installs the ADB tools and udev rules; the AUR builds (WiVRn,
  xrizer, ALVR) are skipped in the container test.
- Debian/EL run with the defaults and verify that nothing is installed.

## Notes

- The WiVRn headset client and PC server must run the same WiVRn version.
  On a Meta Quest, install the client from the Meta Store; the dashboard
  wizard links to it.
- WiVRn installs a systemd user service `wivrn` for headless use
  (`systemctl --user enable --now wivrn`). The role does not enable it; the
  dashboard starts the server on demand.

## References

- [WiVRn](https://github.com/WiVRn/WiVRn)
- [xrizer](https://github.com/Supreeeme/xrizer)
- [ALVR](https://github.com/alvr-org/ALVR)
- [ArchWiki: Virtual reality](https://wiki.archlinux.org/title/Virtual_reality)

## License

MIT

## Author

Marc Straube
