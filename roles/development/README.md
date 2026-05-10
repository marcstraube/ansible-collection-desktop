# marcstraube.desktop.development

Install development tools, IDEs, and programming languages.

## Description

Installs and configures a development environment including version control (Git),
programming languages (Python, Node.js, Rust, Go, Java), build tools, IDEs/editors,
database tools, API testing tools, and miscellaneous CLI utilities. Supports per-user
Git configuration with signing key setup.

## Requirements

- ansible-core >= 2.17
- `community.general` collection (for git_config, pipx, pacman modules)
- `kewlfft.aur` collection (for AUR packages on Arch Linux)

## Supported Platforms

| Platform                  | Notes                                       |
|---------------------------|---------------------------------------------|
| Arch Linux                | Full support including AUR packages         |
| Debian Trixie             | Some IDEs require Flatpak or external repos |
| EL 9 (Rocky, Alma, RHEL)  |                                             |
| EL 10 (Rocky, Alma, RHEL) |                                             |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable              | Default | Description                 |
|-----------------------|---------|-----------------------------|
| `development_enabled` | `true`  | Enable the development role |

### Version Control

| Variable                         | Default | Description                            |
|----------------------------------|---------|----------------------------------------|
| `development_git_enabled`        | `true`  | Enable git installation                |
| `development_git_lfs_enabled`    | `true`  | Enable git-lfs support                 |
| `development_github_cli_enabled` | `true`  | Enable GitHub CLI (gh)                 |
| `development_gitlab_cli_enabled` | `true`  | Enable GitLab CLI (glab)               |
| `development_git_config`         | `{...}` | Git global configuration key/value map |

### Programming Languages

| Variable                      | Default | Description                           |
|-------------------------------|---------|---------------------------------------|
| `development_python_enabled`  | `true`  | Enable Python installation            |
| `development_python_tools`    | `[]`    | Python tools via pipx (non-Arch)      |
| `development_nodejs_enabled`  | `true`  | Enable Node.js                        |
| `development_rust_enabled`    | `false` | Enable Rust installation              |
| `development_rust_components` | `[]`    | Rust components via rustup (non-Arch) |
| `development_go_enabled`      | `false` | Enable Go installation                |
| `development_java_enabled`    | `false` | Enable Java installation              |

### Build Tools

| Variable                    | Default | Description                      |
|-----------------------------|---------|----------------------------------|
| `development_make_enabled`  | `true`  | Enable make and core build tools |
| `development_cmake_enabled` | `false` | Enable cmake                     |
| `development_meson_enabled` | `false` | Enable meson                     |
| `development_ninja_enabled` | `false` | Enable ninja                     |

### IDEs and Editors

| Variable                                | Default | Description              |
|-----------------------------------------|---------|--------------------------|
| `development_vscode_enabled`            | `false` | Enable VS Code           |
| `development_vscodium_enabled`          | `true`  | Enable VSCodium          |
| `development_jetbrains_toolbox_enabled` | `false` | Enable JetBrains Toolbox |
| `development_phpstorm_enabled`          | `false` | Enable PHPStorm          |
| `development_zed_enabled`               | `false` | Enable Zed Editor        |

### Database Tools

| Variable                      | Default | Description    |
|-------------------------------|---------|----------------|
| `development_dbeaver_enabled` | `false` | Enable DBeaver |
| `development_pgadmin_enabled` | `false` | Enable pgAdmin |

### API Tools

| Variable                       | Default | Description     |
|--------------------------------|---------|-----------------|
| `development_httpie_enabled`   | `true`  | Enable httpie   |
| `development_postman_enabled`  | `false` | Enable Postman  |
| `development_insomnia_enabled` | `false` | Enable Insomnia |
| `development_bruno_enabled`    | `false` | Enable Bruno    |

### Misc Tools

| Variable                         | Default | Description                        |
|----------------------------------|---------|------------------------------------|
| `development_jq_enabled`         | `true`  | Enable jq JSON processor           |
| `development_yq_enabled`         | `true`  | Enable yq YAML processor           |
| `development_direnv_enabled`     | `true`  | Enable direnv directory-based envs |
| `development_pre_commit_enabled` | `true`  | Enable pre-commit git hooks        |
| `development_shellcheck_enabled` | `true`  | Enable shellcheck linter           |

### User Configuration

| Variable            | Default | Description                          |
|---------------------|---------|--------------------------------------|
| `development_users` | `[]`    | Users to configure with git settings |

Each user entry supports:

| Key               | Required | Description        |
|-------------------|----------|--------------------|
| `username`        | yes      | System username    |
| `git_name`        | no       | Git user.name      |
| `git_email`       | no       | Git user.email     |
| `git_signing_key` | no       | GPG signing key ID |

## Tags

| Tag                     | Scope                      |
|-------------------------|----------------------------|
| `development`           | All role tasks             |
| `development:git`       | Version control tasks      |
| `development:languages` | Programming language tasks |
| `development:build`     | Build tools tasks          |
| `development:ides`      | IDE installation tasks     |
| `development:tools`     | Misc tools tasks           |
| `development:users`     | User configuration tasks   |

## Example Playbook

```yaml
- name: Include development role
  ansible.builtin.include_role:
    name: marcstraube.desktop.development
  tags:
    - development
  when: development_enabled | default(true) | bool
```

### Minimal Development Setup

```yaml
- name: Include development role
  ansible.builtin.include_role:
    name: marcstraube.desktop.development
  vars:
    development_rust_enabled: true
    development_users:
      - username: 'johndoe'
        git_name: 'John Doe'
        git_email: 'john@example.com'
        git_signing_key: '0x1234567890ABCDEF'
  tags:
    - development
  when: development_enabled | default(true) | bool
```

## Testing

```bash
cd roles/development
molecule test
```

Driver: `podman` | Platforms: Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
