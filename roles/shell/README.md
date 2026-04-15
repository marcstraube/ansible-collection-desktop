# shell

Install and configure shells (Zsh, Fish, Bash) and Starship prompt with modern CLI tools.

## Requirements

None.

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

| Variable        | Default | Description           |
|-----------------|---------|-----------------------|
| `shell_enabled` | `true`  | Enable the shell role |

### Default Shell

| Variable                 | Default     | Description                                               |
|--------------------------|-------------|-----------------------------------------------------------|
| `shell_default`          | `'zsh'`     | Default shell for users: zsh, fish, bash                  |
| `shell_users`            | `[]`        | Users to change shell (empty = all from users_list)       |
| `shell_user_config_mode` | `'managed'` | User config mode: managed, initial (if absent), disabled  |

### Zsh

| Variable                     | Default    | Description                                |
|------------------------------|------------|--------------------------------------------|
| `shell_zsh_enabled`          | `true`     | Enable Zsh installation                    |
| `shell_zsh_plugins`          | `[...]`    | Zsh plugins (completions, autosuggestions) |
| `shell_zsh_grml_enabled`     | `false`    | Enable grml-zsh-config (Arch ISO defaults) |
| `shell_zsh_skeleton_enabled` | `false`    | Enable custom .zshrc skeleton deployment   |

### Fish

| Variable             | Default | Description              |
|----------------------|---------|--------------------------|
| `shell_fish_enabled` | `false` | Enable Fish installation |

### Bash

| Variable                        | Default | Description            |
|---------------------------------|---------|------------------------|
| `shell_bash_completion_enabled` | `true`  | Enable bash-completion |

### Starship

| Variable                        | Default           | Description                                |
|---------------------------------|-------------------|--------------------------------------------|
| `shell_starship_enabled`        | `true`            | Enable Starship prompt installation        |
| `shell_starship_config_enabled` | `false`           | Enable Starship config deployment          |
| `shell_starship_preset`         | `''`              | Starship preset (see docs for options)     |
| `shell_starship_shells`         | `['zsh', 'bash']` | Configure Starship for these shells        |

### Additional Tools

| Variable                 | Default | Description                               |
|--------------------------|---------|-------------------------------------------|
| `shell_fzf_enabled`      | `true`  | Enable fzf (fuzzy finder)                 |
| `shell_zoxide_enabled`   | `false` | Enable zoxide (smarter cd)                |
| `shell_eza_enabled`      | `false` | Enable eza (modern ls)                    |
| `shell_bat_enabled`      | `false` | Enable bat (cat with syntax highlighting) |
| `shell_fd_enabled`       | `false` | Enable fd (modern find)                   |
| `shell_ripgrep_enabled`  | `false` | Enable ripgrep (modern grep)              |
| `shell_tldr_enabled`     | `false` | Enable tldr (simplified man pages)        |

## Tags

| Tag             | Description              |
|-----------------|--------------------------|
| `shell`         | All shell tasks          |
| `shell:install` | Package installation     |
| `shell:users`   | User shell configuration |

## Example Playbook

```yaml
- hosts: workstations
  become: true
  tasks:
    - name: Include shell role
      ansible.builtin.include_role:
        name: marcstraube.desktop.shell
      tags:
        - shell
      when: shell_enabled | default(true) | bool
```

## Testing

```bash
cd collections/ansible_collections/marcstraube/desktop
molecule test -s default -- --limit shell-archlinux
```

## License

MIT

## Author

Marc Straube
