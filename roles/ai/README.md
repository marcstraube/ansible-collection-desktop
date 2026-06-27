# marcstraube.desktop.ai

Install AI development tools.

## Description

Installs AI CLI tools, desktop applications, and local inference engines.
Supports Claude Code, Gemini CLI, OpenAI Codex, OpenCode, Aider, Ollama,
LM Studio, Claude Desktop, OpenCode Desktop, and ComfyUI (Stable Diffusion).

On Arch Linux, tools are installed via native packages (AUR/community/extra).
On Debian and Rocky Linux, tools are installed via npm, pipx, install scripts,
or direct .deb/.rpm downloads from GitHub releases.

API keys are managed by the user via environment variables (not by this role).

## Requirements

- ansible-core >= 2.17
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

| Variable                          | Default | Description                           |
| --------------------------------- | ------- | ------------------------------------- |
| `ai_claude_code_enabled`            | `true`  | Install Claude Code                                 |
| `ai_gemini_cli_enabled`             | `false` | Install Gemini CLI                                  |
| `ai_codex_enabled`                  | `false` | Install OpenAI Codex CLI                            |
| `ai_opencode_enabled`               | `false` | Install OpenCode CLI                                |
| `ai_opencode_claude_auth_enabled`   | `false` | OpenCode auth plugin for Claude creds               |
| `ai_opencode_gemini_auth_enabled`   | `false` | OpenCode auth plugin for Gemini creds               |
| `ai_aider_enabled`                  | `false` | Install Aider (pair programming)                    |
| `ai_claude_cowork_service_enabled`  | `false` | Install Claude Cowork Service (Arch only, AUR)      |

### Desktop Applications

| Variable                      | Default | Description                                  |
| ----------------------------- | ------- | -------------------------------------------- |
| `ai_claude_desktop_enabled`   | `false` | Install Claude Desktop (Arch only)           |
| `ai_opencode_desktop_enabled` | `false` | Install OpenCode Desktop (AUR / .deb / .rpm) |

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
- **Debian / Rocky Linux**: from-source install. The role creates the
  service user/group, clones the upstream ComfyUI repo to
  `ai_comfyui_install_dir`, builds a Python virtual environment, and
  installs PyTorch wheels selected by `ai_comfyui_gpu`. All variables
  above apply.

**ComfyUI-Manager** is installed via manual git-clone on both paths
because no upstream package exists yet (see `tasks/comfyui-archlinux.yml`
for the documented exception to the project's "Arch installs go through
repos or AUR" rule).

## Tags

| Tag          | Scope                              |
| ------------ | ---------------------------------- |
| `ai`         | All AI tasks                       |
| `ai:cli`     | CLI tool installation              |
| `ai:desktop` | Desktop application installation   |
| `ai:local`   | Local AI tools (Ollama, LM Studio) |
| `ai:comfyui` | ComfyUI installation               |

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
