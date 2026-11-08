# marcstraube.desktop.ai

Install AI development tools.

## Description

Installs AI CLI tools, desktop applications, and local inference engines.
Supports Claude Code, Antigravity, OpenAI Codex, OpenCode, Aider,
Ollama, whisper.cpp, the Hugging Face CLI, LM Studio, Claude Desktop (Chat,
Cowork and Claude Code), OpenCode Desktop, and ComfyUI (Stable Diffusion).

On Arch Linux, tools are installed via native packages (AUR/community/extra).
On Debian and Rocky Linux, tools are installed via npm, pipx, install scripts,
or direct .deb/.rpm downloads from GitHub releases.

API keys are managed by the user via environment variables (not by this role).

## Requirements

- ansible-core >= 2.19
- `community.general` collection (npm, pipx, pacman, ini_file modules)
- `ansible.posix` collection (fstab mount of the Ollama model subvolume)
- `btrfs-progs` on BTRFS hosts (creating the model subvolumes)
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
| `ai_enabled` | `false` | Enable/disable AI role |

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
| `ai_aider_model`                   | `''`    | Default model in the per-user Aider config     |
| `ai_aider_set_env`                 | `{}`    | Provider environment (Aider `set-env`)         |
| `ai_opencode_providers`            | `{}`    | OpenAI-compatible model servers for OpenCode   |
| `ai_opencode_model`                | `''`    | Default OpenCode model (`<provider>/<model>`)  |

**Aider model server.** For each `ai_users` entry the role writes
`~/.aider.conf.yml` (mode `0600`) with `model:` and the `set-env:` list when
either variable is set (see [User Configuration](#user-configuration)). This
points Aider at a model served by another host:

```yaml
# Ollama
ai_aider_model: 'ollama_chat/qwen2.5-coder:32b'
ai_aider_set_env:
  OLLAMA_API_BASE: 'http://ollama.example.com:11434'

# LM Studio (the client needs a non-empty key even without authentication)
ai_aider_model: 'lm_studio/qwen2.5-coder-32b-instruct'
ai_aider_set_env:
  LM_STUDIO_API_BASE: 'http://lmstudio.example.com:1234/v1'
  LM_STUDIO_API_KEY: 'dummy-api-key'  # pragma: allowlist secret
```

**OpenCode model server.** For each `ai_users` entry the role writes the
`provider` block and the default `model` into
`~/.config/opencode/opencode.jsonc` (mode `0600`), a file of the role's own.
OpenCode merges it with the user's `opencode.json` next to it, which the role
never touches and which wins on a conflict. Every provider talks to an
OpenAI-compatible server through `@ai-sdk/openai-compatible`; `context` and
`output` become the model's `limit` and are set together or not at all, as
OpenCode rejects a limit with only one of them. `api_key` is only needed when
LM Studio runs with authentication:

```yaml
ai_opencode_providers:
  ollama:
    name: 'Ollama'
    base_url: 'http://localhost:11434/v1'
    models:
      - id: 'qwen3-coder:30b'
        name: 'Qwen3-Coder 30B'
        context: 32768
        output: 8192
  lmstudio:
    name: 'LM Studio'
    base_url: 'http://lmstudio.example.com:1234/v1'
    api_key: '{{ lmstudio_api_key }}'
    models:
      - id: 'qwen3-coder-30b-a3b-instruct'
ai_opencode_model: 'ollama/qwen3-coder:30b'
```

- **Model requirements:** OpenCode is an agent: the model has to call tools
  reliably and needs a context window of at least 32k tokens. The context
  length is set on the server — `OLLAMA_CONTEXT_LENGTH` in
  `ai_ollama_environment`, or the context length LM Studio loads the model
  with. Aider also works with weaker models and without tool calling.
- **Model IDs** differ by server: Ollama uses the full model name (for
  example `hf.co/<user>/<repo>:<quant>`), LM Studio its model key, which
  `curl <server>/v1/models` lists. Models linked from Ollama (see below)
  appear in LM Studio without the `ollama/` directory prefix.

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

| Variable                     | Default | Description                                                     |
| ---------------------------- | ------- | --------------------------------------------------------------- |
| `ai_ollama_enabled`          | `false` | Install Ollama LLM server                                       |
| `ai_ollama_models`           | `[]`    | Models to pull after install                                    |
| `ai_ollama_service_enabled`  | `true`  | Enable Ollama systemd service                                   |
| `ai_ollama_backend`          | `'cpu'` | Backend or list of: `rocm`, `vulkan`, `cuda`, `cpu` (Arch only) |
| `ai_ollama_environment`      | `{}`    | Environment variables for the Ollama server (systemd drop-in)   |
| `ai_ollama_models_dir`       | `''`    | Model directory (empty: package default)                        |
| `ai_ollama_host`             | `''`    | Listen address (empty: `127.0.0.1`)                             |
| `ai_ollama_port`             | `11434` | Listen port                                                     |
| `ai_whisper_enabled`         | `false` | Install whisper.cpp speech recognition (Arch only)              |
| `ai_whisper_backend`         | `'cpu'` | Backend or list of: `rocm`, `vulkan`, `cuda`, `cpu` (Arch only) |
| `ai_huggingface_cli_enabled` | `false` | Install the Hugging Face CLI `hf` (Arch only)                   |
| `ai_lmstudio_enabled`        | `false` | Install LM Studio (Arch only)                                   |
| `ai_lmstudio_models_dir`     | `''`    | Model directory per user (empty: LM Studio's own setting)       |
| `ai_lmstudio_host`           | `''`    | Server address per user (empty: LM Studio's own setting)        |
| `ai_lmstudio_port`           | `''`    | Server port per user (empty: LM Studio's own setting)           |
| `ai_lmstudio_models`         | `[]`    | GGUF files to download per user (`repo`, `file`)                |
| `ai_huggingface_token`       | `''`    | Token for gated or private Hugging Face repositories            |
| `ai_lmstudio_ollama_models`  | `[]`    | Ollama models to link into LM Studio                            |

**Ollama backend** (`ai_ollama_backend`):

- **Arch Linux**: the `ollama` package runs inference on the CPU. The GPU
  backends ship as separate packages in `extra`, and the role installs the
  package of every selected backend next to `ollama`: `ollama-rocm` (AMD;
  roughly 3 GiB plus the ROCm libraries), `ollama-vulkan` (any Vulkan GPU,
  roughly 44 MiB) or `ollama-cuda` (NVIDIA; roughly 1 GiB plus CUDA). `cpu`
  installs nothing extra. ROCm supports RDNA 3 and newer AMD cards without
  overrides. The role restarts Ollama when the packages change, since Ollama
  loads its backends at startup. Switching the backend installs the new
  package and leaves the previous one in place.
- **Several backends**: a list installs the backend packages side by side,
  for example ROCm and Vulkan for applications that support only one of
  them. Ollama can then see the same GPU once per backend; the application
  selects the device.
- **Debian / EL**: the upstream install script detects AMD and NVIDIA GPUs
  itself and installs the matching runtime; the variable has no effect.

```yaml
ai_ollama_backend: ['rocm', 'vulkan']   # several backends side by side
```

**Ollama server settings** (`ai_ollama_environment`):

Ollama reads its server settings from environment variables. The role renders
each entry as an `Environment=` line into the systemd drop-in
`/etc/systemd/system/ollama.service.d/ansible.conf` and restarts Ollama when
the drop-in changes. Both the Arch
package and the upstream install script ship `ollama.service`, so this works
on every platform.

```yaml
ai_ollama_environment:
  OLLAMA_CONTEXT_LENGTH: '32768'   # default context window
  OLLAMA_FLASH_ATTENTION: '1'      # flash attention
  OLLAMA_KEEP_ALIVE: '30m'         # keep models loaded
```

See the [Ollama FAQ](https://docs.ollama.com/faq) for all settings.

**Ollama model directory and address** (`ai_ollama_models_dir`,
`ai_ollama_host`, `ai_ollama_port`):

- `ai_ollama_models_dir` creates the directory for the `ollama` service user
  and renders `OLLAMA_MODELS` into the same drop-in. Empty keeps the package
  default: `/var/lib/ollama` on Arch Linux, `/usr/share/ollama/.ollama/models`
  with the install script.
- `ai_ollama_host` and `ai_ollama_port` render `OLLAMA_HOST` when either
  differs from `127.0.0.1:11434`. `0.0.0.0` serves the whole network; a
  changed port needs the matching firewalld service or port.
- The drop-in also sets `RequiresMountsFor=` on the model directory: Ollama
  waits for its file system and does not start without it, instead of
  filling the empty directory below the mount point. This matters for a
  directory on a second disk mounted with `nofail` or on demand.
- Setting `OLLAMA_MODELS` or `OLLAMA_HOST` in `ai_ollama_environment` as well
  fails the run. Inventories that set them only there keep working.
- `ai_ollama_models` reports a change only when a model is new or its
  manifest changed: the role compares the model ID `ollama list` shows
  before and after each pull.

**Model directories on BTRFS.** Models are large and can be downloaded
again, so the role keeps them out of snapshots. A model directory on BTRFS
that does not exist yet or is empty becomes its own subvolume:

- **Ollama**, on the root filesystem: a top-level subvolume
  (`<root subvolume base>/<path>`, e.g. `@/var/lib/ollama`) mounted through
  `/etc/fstab` with the options of the root filesystem plus
  `nosuid,nodev,noexec`. A subvolume nested below `/` would live inside the
  root snapshot of a snapper rollback layout and stay behind on
  `snapper rollback`. On any other mount (`/srv`, `/home`) the subvolume is
  nested.
- **LM Studio**, below the user's home: a nested subvolume with mode `0700`,
  which snapshots of the home skip.
- No NoCOW: model files are written once and keep checksums and compression.

**Disk speed.** A hard disk works for the model directories: a model is read
once when it loads, and inference runs from RAM or VRAM. A 20 GB model loads
in about two minutes from a hard disk, against seconds from an NVMe SSD.
Ollama unloads a model after five idle minutes (`OLLAMA_KEEP_ALIVE`), so the
next prompt waits for the load again; layers kept in RAM through mmap are
read from the disk again whenever memory runs short. Each tool has one model
directory. To keep only some LM Studio models on another disk, move their
repository directory (`<models dir>/<publisher>/<repo>`) there and link it
back; the role downloads through the link and keeps it. Ollama's blobs are
shared between models and cannot be split this way.

A directory that already holds models stays as it is; the role never moves
data. To move it onto a subvolume, stop the application (`systemctl stop
ollama`, quit LM Studio), move the directory aside, run the role (or create
the subvolume yourself), move the contents back and remove the old
directory. On Arch Linux `/var/lib/ollama` is also the home of the service
user and holds its key (`.ollama/id_ed25519`) after the first start — move it
along with the models.

**LM Studio settings** (`ai_lmstudio_models_dir`, `ai_lmstudio_host`,
`ai_lmstudio_port`): LM Studio writes its settings files itself, so the role
only sets the keys whose variables are set and leaves everything else —
including a value set in the app while the variable is empty — alone:

| File                                            | Keys                        |
| ----------------------------------------------- | --------------------------- |
| `~/.lmstudio/settings.json`                     | `downloadsFolder`           |
| `~/.lmstudio/.internal/http-server-config.json` | `networkInterface`, `port`  |

`ai_lmstudio_models_dir` is an absolute path or relative to the home. Changes
apply on the next start of LM Studio. `lms server start` without `--bind`
stores `127.0.0.1` as `networkInterface`, overriding the role's value until
the next run; start the server with `--bind <address>` instead.

**LM Studio models** (`ai_lmstudio_models`): each entry names a GGUF `file`
in a Hugging Face `repo`. The role downloads it per user with
`hf download --local-dir` into `<models dir>/<publisher>/<repo>/<file>`, the
layout LM Studio expects, and skips files that are present. It needs the
Hugging Face CLI (`ai_huggingface_cli_enabled`). Public repositories need no
token; gated or private ones need `ai_huggingface_token`, which is passed to
the download only and never written to disk.

```yaml
ai_lmstudio_models:
  - repo: 'lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF'
    file: 'Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf'
```

**Share Ollama models with LM Studio** (`ai_lmstudio_ollama_models`): the
model directories stay separate by default. Every listed Ollama model is
linked into `<models dir>/ollama/<model>-<tag>/` — the GGUF model layer as
`<model>-<tag>.gguf` and, for vision models, the projector as
`mmproj-<model>-<tag>.gguf`. Ollama stores its blobs with mode `0644`, so
every LM Studio user can read them. The `ollama/` directory follows the list:
links of removed entries are deleted, and links move when a newer pull
replaces a blob. Ollama's own files are never changed.

```yaml
ai_ollama_models:
  - 'hf.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M'
ai_lmstudio_ollama_models:
  - 'hf.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M'
```

- **Trade-offs:** one copy on disk and one download, against links that
  depend on the Ollama model staying installed — removing it from Ollama
  breaks the model in LM Studio.
- **Source per use:** pull shared models from Hugging Face as
  `hf.co/<user>/<gguf-repo>:<quant>`; Ollama stores the repository's GGUF
  files unchanged, the same files LM Studio would download. Models used only
  by Ollama come from Ollama's own library: library models carry Ollama's
  model-specific prompt rendering and output parsing, while `hf.co` models
  use the chat template embedded in the GGUF, so options such as `think` may
  be unavailable.
- **Compatibility:** library models in Ollama's own format cannot be loaded
  by LM Studio. `ollama ps` shows the runner of a loaded model; `llamacpp`
  indicates a standard GGUF.

**whisper.cpp** (`ai_whisper_enabled`, `ai_whisper_backend`):

- **Arch Linux**: installs `whisper-cpp` from `extra`. It depends on `ggml`,
  which brings the CPU backend; the role installs every selected GPU backend
  next to it: `ggml-hip` (AMD; pulls in `rocm-hip-runtime`, roughly 1.3 GiB),
  `ggml-vulkan` (any Vulkan GPU, roughly 44 MiB) or `ggml-cuda` (NVIDIA;
  roughly 150 MiB plus CUDA). `cpu` installs nothing extra. A list such as
  `ai_whisper_backend: ['rocm', 'vulkan']` installs several backends side by
  side, for applications that support only one of them. ggml loads every
  installed backend at runtime, so the same GPU can show up once per backend;
  applications select the device themselves.
- **Debian / EL**: whisper.cpp is not packaged (Debian ships it from forky
  on), so the toggle is a no-op. Build it from source:
  <https://github.com/ggml-org/whisper.cpp>.

**Hugging Face CLI** (`ai_huggingface_cli_enabled`):

`hf` downloads models and datasets from the Hugging Face Hub, for example GGUF
models for whisper.cpp or llama.cpp-based tools and checkpoints for ComfyUI.
Gated models need an access token: `hf auth login` stores it per user in
`~/.cache/huggingface/token`; the role does not manage it.

- **Arch Linux**: installs `python-huggingface-hub` from `extra`, which ships
  `hf`.
- **Debian / EL**: the CLI is not packaged, so the toggle is a no-op. Install
  it per user with `pipx install huggingface_hub`.

### ComfyUI (Stable Diffusion)

| Variable                      | Default                 | Description                                                |
| ----------------------------- | ----------------------- | ---------------------------------------------------------- |
| `ai_comfyui_enabled`          | `false`                 | Install ComfyUI                                            |
| `ai_comfyui_backend`          | `'cuda'`                | Compute backend: `cuda`, `rocm` or `cpu`                   |
| `ai_comfyui_version`          | `'master'`              | Git branch/tag (manual path only)                          |
| `ai_comfyui_install_dir`      | `'/opt/comfyui'`        | Installation directory (manual path only)                  |
| `ai_comfyui_home`             | `'/var/lib/comfyui'`    | Service user home (manual path only; FHS state directory)  |
| `ai_comfyui_listen`           | `'127.0.0.1'`           | Listen address                                             |
| `ai_comfyui_port`             | `8188`                  | Web UI port                                                |
| `ai_comfyui_user`             | `'comfyui'`             | Service user (manual path only)                            |
| `ai_comfyui_group`            | `'comfyui'`             | Service group (manual path only)                           |
| `ai_comfyui_manager_enabled`  | `true`                  | Install ComfyUI-Manager                                    |
| `ai_comfyui_service_enabled`  | `true`                  | Enable systemd service                                     |

> **Deprecation:** `ai_comfyui_gpu` (`nvidia`, `amd`, `cpu`) is deprecated and
> will be removed in v4.0.0. Use `ai_comfyui_backend` instead: `nvidia` becomes
> `cuda`, `amd` becomes `rocm`, `cpu` stays `cpu`. While `ai_comfyui_gpu` is
> set, the role maps its value and prints a warning.
>
> **Default change:** the default of `ai_comfyui_backend` changes from `cuda`
> to `cpu` in v4.0.0, so it works on every host. Set
> `ai_comfyui_backend: 'cuda'` explicitly to keep CUDA.

**Install path differs by OS family:**

- **Arch Linux**: installs the AUR `comfyui` package via `kewlfft.aur.aur`.
  The PKGBUILD owns the install dir (`/opt/comfyui`), the service user
  (`comfy`), the Python venv, the PyTorch wheel selection (driven by
  `COMFYUI_GPU`, set to `ai_comfyui_backend`), and the
  systemd unit. Inventory variables marked *(manual path only)* in the
  table above are **not honored** on Arch — they are fixed by the AUR
  PKGBUILD.
- **Debian** (`ai_comfyui_backend: cuda` or `cpu`): from-source install with
  native PyTorch. The role installs `python3-torch-cuda` (cuda) or
  `python3-torch` (cpu) plus `python3-torchvision` and `python3-torchaudio`
  from Debian's repositories, then builds a `--system-site-packages` venv so
  ComfyUI sees them. ComfyUI's own requirements are installed into the venv;
  torch is already satisfied by the native packages. All *(manual path only)*
  variables above apply.
- **Debian with `ai_comfyui_backend: rocm`, and all Rocky Linux / EL hosts**:
  **unsupported**. No complete native PyTorch stack
  (torch/torchvision/torchaudio) is packaged there, and the upstream pip wheel
  index is fragile against Python version drift. The role fails fast with a
  clear message (see issue #122). Use Arch Linux for AMD/ROCm.

**ComfyUI-Manager** (`ai_comfyui_manager_enabled`):

- **Arch Linux**: AUR package `comfyui-manager`. It installs the manager
  into the venv of the `comfyui` package and ships a systemd drop-in that
  starts `comfyui.service` with `--enable-manager`. The role restarts
  ComfyUI after the package changes. The `cm-cli` command runs the
  manager's CLI as the service user, e.g.
  `sudo -u comfy cm-cli show installed`.
- **Debian**: git clone into `custom_nodes/ComfyUI-Manager` as the service
  user.

### User Configuration

For each `ai_users` entry the role writes the per-user configs of the
enabled tools:

- **Claude Desktop:** copies the packaged entry into
  `~/.local/share/applications/`, appends `--password-store=<backend>` to
  every `Exec=` line and refreshes the desktop database — skipping that last
  step breaks the `claude://` sign-in redirect.
- **Aider:** `~/.aider.conf.yml` from `ai_aider_model` and `ai_aider_set_env`.
- **OpenCode:** `~/.config/opencode/opencode.jsonc` from
  `ai_opencode_providers` and `ai_opencode_model`.
- **LM Studio:** the settings, downloads and Ollama links described under
  [Local AI / Inference](#local-ai--inference).

| Variable                             | Default                       | Description                          |
| ------------------------------------ | ----------------------------- | ------------------------------------ |
| `ai_users`                           | `[]`                          | Users to configure                   |
| `ai_user_config_mode`                | `'initial'`                   | Fallback mode for the tool defaults  |
| `ai_claude_desktop_user_config_mode` | `'{{ ai_user_config_mode }}'` | Default mode of the Claude entry     |
| `ai_aider_user_config_mode`          | `'{{ ai_user_config_mode }}'` | Default mode of the Aider config     |
| `ai_opencode_user_config_mode`       | `'managed'`                   | Default mode of the OpenCode config  |
| `ai_lmstudio_user_config_mode`       | `'merged'`                    | Default mode of the LM Studio files  |

Each user entry supports:

| Key              | Required | Description                                             |
| ---------------- | -------- | ------------------------------------------------------- |
| `username`       | yes      | System username                                         |
| `mode`           | no       | Mode for every tool of this user (overrides defaults)   |
| `password_store` | no       | Per-user override of `ai_claude_desktop_password_store` |

Left empty, `ai_users` derives from `users_list` entries carrying an `ai`
attribute (system users excluded):

```yaml
users_list:
  - name: 'johndoe'
    ai: true
```

> **Deprecation:** deriving `ai_users` from the `users_list` `ai` attribute is
> deprecated and will be removed in v4.0.0. The role prints a warning while it
> derives users this way. From v4.0.0 an empty `ai_users` means no users; set
> `ai_users` explicitly. See #304.

Mode semantics:

| Mode       | First run                          | Subsequent runs                                  |
| ---------- | ---------------------------------- | ------------------------------------------------ |
| `managed`  | deploy the whole file              | overwrite the whole file (always reconcile)      |
| `merged`   | deploy the role-owned keys         | set the role-owned keys, keep all others         |
| `initial`  | deploy if the file is absent       | leave the user's own edits alone                 |
| `disabled` | skip                               | skip                                             |

A user's `mode` applies to every tool; without it each tool uses its own
default. `initial` gates on the file itself, not on whether the account was
created in the same run, so a tag-scoped run still deploys. In `managed` mode
the Aider config and the role's OpenCode file are removed when none of their
variables is set. Nothing is written to any home directory while `ai_users`
is empty or none of the tools is enabled.

**Choosing a mode.** A file of the role's own is always the cleaner way:
`managed` then reconciles it completely, including removals, and the user's
settings live in a file the role never touches. OpenCode supports this, so
the role keeps its keys in `opencode.jsonc` and `merged` behaves like
`managed` there. `merged` is for files the application reads only in one
place, where the role still has to add or update its keys — the Aider
config, the Claude Desktop entry and LM Studio's settings.

**Role-owned keys in `merged` mode:**

| Config                         | Keys                                          |
| ------------------------------ | --------------------------------------------- |
| `~/.aider.conf.yml`            | `model`, `set-env`                            |
| Claude Desktop entry           | `Exec` of every group                         |
| LM Studio settings (see above) | `downloadsFolder`, `networkInterface`, `port` |

- A key is set while its variable is set, and written as a whole: an entry
  dropped from `ai_aider_set_env` also leaves `set-env`.
- `merged` never removes a key. The role cannot tell a value it wrote from
  one the user set, so an empty variable leaves the key as it is. To remove
  a value the role wrote, delete it by hand or run the user once in
  `managed` mode.
- The Aider config and the Claude Desktop entry carry a header naming the
  keys the role sets; in the Aider config it disappears once none of them is
  set:

  ```yaml
  # Partly managed by Ansible (marcstraube.desktop.ai): model, set-env
  # Ansible updates these keys on every run; all other keys are yours.
  ```

- Writing a file back drops the comments of the user's own in
  `~/.aider.conf.yml` and may reorder keys on the first run. A file the role
  cannot parse fails the run and stays unchanged.
- An `opencode.jsonc` the role did not write (it lacks the role's marker
  line) is never replaced or removed: the run fails and names the file. Move
  its settings to `opencode.json`, or use `initial` or `disabled` for that
  user.

## Tags

| Tag          | Scope                                                             |
| ------------ | ----------------------------------------------------------------- |
| `ai`         | All AI tasks                                                      |
| `ai:cli`     | CLI tool installation                                             |
| `ai:desktop` | Desktop application installation                                  |
| `ai:local`   | Local AI tools (Ollama, whisper.cpp, Hugging Face CLI, LM Studio) |
| `ai:comfyui` | ComfyUI installation                                              |
| `ai:users`   | Per-user Claude Desktop, Aider, OpenCode and LM Studio config     |

## Example Playbook

```yaml
- name: AI tools
  hosts: workstations
  tasks:
    - name: AI | Include ai role
      ansible.builtin.include_role:
        name: marcstraube.desktop.ai
      tags: [ai]
      when: ai_enabled | default(false) | bool
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
