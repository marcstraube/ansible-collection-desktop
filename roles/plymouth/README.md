# marcstraube.desktop.plymouth

Install and configure Plymouth boot splash screen.

## Description

Installs Plymouth, configures the boot splash theme, and manages kernel parameters
for a graphical boot experience. On Arch Linux, automatically inserts the plymouth
hook into mkinitcpio and detects GPG hook incompatibility. On Debian and RedHat,
plymouth integrates automatically via initramfs-tools/dracut respectively.

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
| `plymouth_enabled` | `true`  | Enable the plymouth role |

### Theme

| Variable         | Default  | Description             |
|------------------|----------|-------------------------|
| `plymouth_theme` | `'bgrt'` | Plymouth theme to apply |

### Packages

| Variable                  | Default | Description                           |
|---------------------------|---------|---------------------------------------|
| `plymouth_extra_packages` | `[]`    | Additional packages (e.g. AUR themes) |

### Kernel Parameters

| Variable                         | Default | Description                                                   |
|----------------------------------|---------|---------------------------------------------------------------|
| `plymouth_kernel_params_enabled` | `true`  | Manage 'quiet splash' in GRUB_CMDLINE_LINUX_DEFAULT           |

### Initramfs (Arch Linux)

| Variable                 | Default  | Description                                                           |
|--------------------------|----------|-----------------------------------------------------------------------|
| `plymouth_hook_position` | `'auto'` | Insert plymouth hook after this hook ('auto' = after udev or systemd) |

## Tags

| Tag                   | Scope                              |
|-----------------------|------------------------------------|
| `plymouth`            | All role tasks                     |
| `plymouth:install`    | Package installation               |
| `plymouth:configure`  | Configuration and mkinitcpio hooks |
| `plymouth:kernel`     | Kernel parameter management        |

## Example Playbook

```yaml
- name: Include plymouth role
  ansible.builtin.include_role:
    name: marcstraube.desktop.plymouth
  tags: [plymouth]
  when: plymouth_enabled | default(true) | bool
```

## Testing

```bash
cd roles/plymouth
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## Notes

Plymouth may not be compatible with all disk encryption setups. Systems using
LUKS full disk encryption with GPG key unlock should disable Plymouth
(`plymouth_enabled: false`) as it interferes with the passphrase/key prompt
during early boot.

## License

MIT

## Author

Marc Straube
