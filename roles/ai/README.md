# marcstraube.desktop.ai

Install AI development tools.

## Description

Installs AI CLI tools, desktop applications, and local inference engines.
Supports Claude Code, Antigravity, OpenAI Codex, OpenCode, Aider,
Ollama, LM Studio, Claude Desktop (Chat, Cowork and Claude Code),
OpenCode Desktop, and ComfyUI (Stable Diffusion).

On Arch Linux, tools are installed via native packages (AUR/community/extra).
On Debian and Rocky Linux, tools are installed via npm, pipx, install scripts,
or direct .deb/.rpm downloads from GitHub releases.

API keys are managed by the user via environment variables (not by this role).

## Requirements

- ansible-core >= 2.19
- `community.general` collection (npm, pipx, pacman modules)
- `kewlfft.aur` collection (AUR packages on Arch Linux)
- Node.js and npm (for CLI tools on non-Arch)
- pipx (for Aider on non-Arch)

## Supported Platforms

| Platform                  | Notes                    |
| ------------------------- | ------------------------ |
| Arch Linux                | Native packages + AUR    |
| Debian Trixie             | npm/pipx/install scripts |
| EL 9 (Rocky, Alma, RHEL)  | npm/pipx/install scripts |
| EL 10 (Rocky, Alma, RHEL) | npm/pipx/install scripts |

## Role Variables

### Role Control

| Variable     | Default | Description            |
| ------------ | ------- | ---------------------- |
| `ai_enabled` | `true`  | Enable/disable AI role |

### CLI Tools

| Variable                           | Default | Description                                    |
| ---------------------------------- | ------- | ---------------------------------------------- |
| `ai_claude_code_enabled`           | `true`  | Install Claude Code                            |
| `ai_antigravity_cli_enabled`       | `false` | Install Antigravity CLI (Arch only, AUR)       |
| `ai_codex_enabled`                 | `false` | Install OpenAI Codex CLI                       |
| `ai_opencode_enabled`              | `false` | Install OpenCode CLI                           |
| `ai_opencode_claude_auth_enabled`  | `false` | OpenCode auth plugin for Claude creds          |
| `ai_opencode_gemini_auth_enabled`  | `false` | OpenCode auth plugin for Gemini creds          |
| `ai_aider_enabled`                 | `false` | Install Aider (pair programming)               |

### Desktop Applications

| Variable                             | Default              | Description                                     |
| ------------------------------------ | -------------------- | ----------------------------------------------- |
| `ai_claude_desktop_enabled`          | `false`              | Install Claude Desktop (Arch only)              |
| `ai_claude_desktop_password_store`   | `'gnome-libsecret'`  | Credential backend for the per-user entry       |
| `ai_antigravity_enabled`             | `false`              | Install Antigravity (Arch only)                 |
| `ai_opencode_desktop_enabled`        | `false`              | Install OpenCode Desktop (AUR / .deb / .rpm)    |

**Claude Desktop ships Cowork.** The `claude-desktop` package covers Chat,
Cowork and Claude Code in one app and pulls in the
`virtiofsd`/`qemu-system-x86`/`edk2-ovmf`/`socat` chain Cowork's VM needs. The
separate `claude-cowork-service` backend is deprecated and unmaintained
upstream, so enabling `ai_claude_desktop_enabled` removes it — the two do not
overlap on files, but its systemd user unit serves a function the app now
provides itself. The same step removes `claude-desktop-bin`, the AUR
package's former name, which would otherwise conflict with the install.

**Credential backend.** Claude Desktop is Chromium-based and picks its
password store from the detected desktop. On compositors it does not
recognize, sign-in data is stored unencrypted and switching sessions logs the
user out. The role's per-user entry pins the backend explicitly:

| Keystore                                              | `password_store`  |
| ----------------------------------------------------- | ----------------- |
| freedesktop Secret Service (KeePassXC, GNOME Keyring) | `gnome-libsecret` |
| KWallet                                               | `kwallet6`        |

### Local AI / Inference

| Variable                    | Default | Description                   |
| --------------------------- | ------- | ----------------------------- |
| `ai_ollama_enabled`         | `false` | Install Ollama LLM server     |
| `ai_ollama_models`          | `[]`    | Models to pull after install  |
| `ai_ollama_service_enabled` | `true`  | Enable Ollama systemd service |
| `ai_lmstudio_enabled`       | `false` | Install LM Studio (Arch only) |

### ComfyUI (Stable Diffusion)

| Variable                      | Default                 | Description                                                |
| ----------------------------- | ----------------------- | ---------------------------------------------------------- |
| `ai_comfyui_enabled`          | `false`                 | Install ComfyUI                                            |
| `ai_comfyui_gpu`              | `'nvidia'`              | GPU backend: `nvidia`, `amd`, or `cpu`                     |
| `ai_comfyui_version`          | `'master'`              | Git branch/tag (manual path only)                          |
| `ai_comfyui_install_dir`      | `'/opt/comfyui'`        | Installation directory (manual path only)                  |
| `ai_comfyui_home`             | `'/var/lib/comfyui'`    | Service user home (manual path only; FHS state directory)  |
| `ai_comfyui_listen`           | `'127.0.0.1'`           | Listen address                                             |
| `ai_comfyui_port`             | `8188`                  | Web UI port                                                |
| `ai_comfyui_user`             | `'comfyui'`             | Service user (manual path only)                            |
| `ai_comfyui_group`            | `'comfyui'`             | Service group (manual path only)                           |
| `ai_comfyui_manager_enabled`  | `true`                  | Install ComfyUI-Manager                                    |
| `ai_comfyui_service_enabled`  | `true`                  | Enable systemd service                                     |

**Install path differs by OS family:**

- **Arch Linux**: installs the AUR `comfyui` package via `kewlfft.aur.aur`.
  The PKGBUILD owns the install dir (`/opt/comfyui`), the service user
  (`comfy`), the Python venv, the PyTorch wheel selection (driven by
  `COMFYUI_GPU={cuda,rocm,cpu}` mapped from `ai_comfyui_gpu`), and the
  systemd unit. Inventory variables marked *(manual path only)* in the
  table above are **not honored** on Arch — they are fixed by the AUR
  PKGBUILD.
- **Debian** (`ai_comfyui_gpu: nvidia` or `cpu`): from-source install with
  native PyTorch. The role installs `python3-torch-cuda` (nvidia) or
  `python3-torch` (cpu) plus `python3-torchvision` and `python3-torchaudio`
  from Debian's repositories, then builds a `--system-site-packages` venv so
  ComfyUI sees them. ComfyUI's own requirements are installed into the venv;
  torch is already satisfied by the native packages. All *(manual path only)*
  variables above apply.
- **Debian with `ai_comfyui_gpu: amd`, and all Rocky Linux / EL hosts**:
  **unsupported**. No complete native PyTorch stack
  (torch/torchvision/torchaudio) is packaged there, and the upstream pip wheel
  index is fragile against Python version drift. The role fails fast with a
  clear message (see issue #122). Use Arch Linux for AMD/ROCm.

**ComfyUI-Manager** is installed via manual git-clone on both paths
because no upstream package exists yet (see `tasks/comfyui-archlinux.yml`
for the documented exception to the project's "Arch installs go through
repos or AUR" rule).

### User Configuration

The role copies the packaged Claude Desktop entry into a user's
`~/.local/share/applications/`, appends `--password-store=<backend>` to every
`Exec=` line and refreshes the desktop database — skipping that last step
breaks the `claude://` sign-in redirect.

| Variable               | Default     | Description                                      |
| ---------------------- | ----------- | ------------------------------------------------ |
| `ai_users`             | `[]`        | Users to configure with a Claude Desktop entry   |
| `ai_user_config_mode`  | `'initial'` | Default mode: `managed` / `initial` / `disabled` |

Each user entry supports:

| Key              | Required | Description                                             |
| ---------------- | -------- | ------------------------------------------------------- |
| `username`       | yes      | System username                                         |
| `mode`           | no       | Per-user override of the global config mode             |
| `password_store` | no       | Per-user override of `ai_claude_desktop_password_store` |

Left empty, `ai_users` derives from `users_list` entries carrying an `ai`
attribute, the standard derivation across the `marcstraube` collections:

```yaml
users_list:
  - name: 'johndoe'
    ai: true
```

Mode semantics:

| Mode       | First run                     | Subsequent runs                            |
| ---------- | ----------------------------- | ------------------------------------------ |
| `managed`  | deploy                        | overwrite (always reconcile)               |
| `initial`  | deploy if the entry is absent | leave the user's own edits alone           |
| `disabled` | skip                          | skip                                       |

`initial` gates on the entry file itself, not on whether the account was
created in the same run, so a tag-scoped run still deploys. Nothing is written
to any home directory while `ai_users` is empty or Claude Desktop is disabled.

## Tags

| Tag          | Scope                              |
| ------------ | ---------------------------------- |
| `ai`         | All AI tasks                       |
| `ai:cli`     | CLI tool installation              |
| `ai:desktop` | Desktop application installation   |
| `ai:local`   | Local AI tools (Ollama, LM Studio) |
| `ai:comfyui` | ComfyUI installation               |
| `ai:users`   | Per-user Claude Desktop entry      |

## Example Playbook

```yaml
- name: AI tools
  hosts: workstations
  tasks:
    - name: AI | Include ai role
      ansible.builtin.include_role:
        name: marcstraube.desktop.ai
      tags: [ai]
      when: ai_enabled | default(true) | bool
```

## Testing

```bash
cd roles/ai
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## License

MIT

## Author

Marc Straube
