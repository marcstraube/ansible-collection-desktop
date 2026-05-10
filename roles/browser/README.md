# marcstraube.desktop.browser

Install and configure web browsers with enterprise policies and hardening.

## Description

Installs and configures web browsers with system-wide enterprise policies for
extension management, privacy hardening, and telemetry control. Supports
Firefox, LibreWolf, Chromium, Brave, Tor Browser, and Zen Browser.

Browser extensions are managed via policies (force-installed, user-installable,
or blocked). Firefox/LibreWolf also support per-user hardening preferences
via `user.js` and system-wide locked preferences via `firefox.cfg`.

LibreWolf, Brave, Tor Browser, and Zen Browser are installed from AUR on
Arch Linux. Tor Browser is available via `torbrowser-launcher` on Debian.
Chromium on Rocky Linux requires EPEL.

## Requirements

- ansible-core >= 2.17
- `community.general` collection (pacman module)
- `kewlfft.aur` collection (Arch Linux AUR packages)
- Rocky Linux requires EPEL to be enabled for Chromium.
  EPEL is managed by the `marcstraube.common.package_management` role.

## Supported Platforms

| Platform       | Firefox | Chromium     | LibreWolf | Brave | Tor    | Zen  |
| -------------- | ------- | ------------ | --------- | ----- | ------ | ---- |
| Arch Linux     | yes     | yes          | AUR       | AUR   | AUR    | AUR  |
| Debian Trixie  | ESR     | yes          | no        | no    | yes    | no   |
| EL 9           | yes     | EPEL         | no        | no    | no     | no   |
| EL 10          | yes     | EPEL         | no        | no    | no     | no   |

## Role Variables

### Role Control

| Variable          | Default | Description         |
| ----------------- | ------- | ------------------- |
| `browser_enabled` | `true`  | Enable/disable role |

### Browsers to Install

| Variable                     | Default     | Description                   |
| ---------------------------- | ----------- | ----------------------------- |
| `browser_firefox_enabled`    | `true`      | Install Firefox               |
| `browser_chromium_enabled`   | `true`      | Install Chromium              |
| `browser_librewolf_enabled`  | `false`     | Install LibreWolf (Arch only) |
| `browser_brave_enabled`      | `false`     | Install Brave (Arch only)     |
| `browser_tor_enabled`        | `false`     | Install Tor Browser           |
| `browser_zen_enabled`        | `false`     | Install Zen Browser (Arch)    |
| `browser_default`            | `'firefox'` | Default browser (xdg)         |

### Firefox Options

| Variable                              | Default | Description                           |
| ------------------------------------- | ------- | ------------------------------------- |
| `browser_firefox_policies_enabled`    | `true`  | Deploy policies.json                  |
| `browser_firefox_user_js_enabled`     | `true`  | Deploy per-user user.js               |
| `browser_firefox_i18n`                | `''`    | Language pack code (empty = none)     |
| `browser_firefox_extensions`          | `{...}` | Extensions with install modes         |
| `browser_firefox_extensions_optional` | `{}`    | Optional extensions (user-selectable) |
| `browser_firefox_preferences`         | `{...}` | Firefox preferences for user.js/cfg   |
| `browser_firefox_policy_settings`     | `{...}` | Additional policies.json settings     |

### LibreWolf Options

| Variable                                      | Default     | Description                      |
| --------------------------------------------- | ----------- | -------------------------------- |
| `browser_librewolf_policies_enabled`          | `true`      | Deploy policies.json             |
| `browser_librewolf_extensions`                | `{...}`     | Extensions (defaults to Firefox) |
| `browser_librewolf_preferences`               | `{}`        | Additional preferences           |
| `browser_librewolf_disable_telemetry`         | `true`      | Disable telemetry                |
| `browser_librewolf_disable_pocket`            | `true`      | Disable Pocket                   |
| `browser_librewolf_disable_firefox_studies`   | `true`      | Disable Firefox studies          |
| `browser_librewolf_homepage`                  | `''`        | Homepage URL (empty = default)   |
| `browser_librewolf_no_default_bookmarks`      | `true`      | Remove default bookmarks         |
| `browser_librewolf_offer_to_save_logins`      | `false`     | Offer to save logins             |
| `browser_librewolf_password_manager`          | `false`     | Built-in password manager        |

### Chromium Options

| Variable                                      | Default     | Description                       |
| --------------------------------------------- | ----------- | --------------------------------- |
| `browser_chromium_policies_enabled`           | `true`      | Deploy policies                   |
| `browser_chromium_wayland_gestures_enabled`   | `true`      | Wayland gesture hook (Arch only)  |
| `browser_chromium_extensions`                 | `{...}`     | Extensions with install modes     |
| `browser_chromium_policy_settings`            | `{...}`     | Additional policy settings        |

### Brave Options

| Variable                              | Default     | Description                       |
| ------------------------------------- | ----------- | --------------------------------- |
| `browser_brave_policies_enabled`      | `true`      | Deploy policies                   |
| `browser_brave_extensions`            | `{...}`     | Extensions (defaults to Chromium) |
| `browser_brave_homepage`              | `''`        | Homepage URL (empty = default)    |
| `browser_brave_signin`                | `0`         | Sign-in: 0=off, 1=on, 2=required  |
| `browser_brave_sync_disabled`         | `true`      | Disable Brave Sync                |
| `browser_brave_metrics`               | `false`     | Metrics reporting                 |
| `browser_brave_safe_browsing`         | `true`      | Safe Browsing                     |
| `browser_brave_password_manager`      | `false`     | Built-in password manager         |
| `browser_brave_autofill_address`      | `false`     | Autofill address forms            |
| `browser_brave_autofill_credit_card`  | `false`     | Autofill credit card forms        |

### Extension Control

| Variable                          | Default     | Description                 |
| --------------------------------- | ----------- | --------------------------- |
| `browser_extension_default_mode`  | `'blocked'` | Default: allowed or blocked |

### User Configuration

| Variable                   | Default     | Description                            |
| -------------------------- | ----------- | -------------------------------------- |
| `browser_users`            | `[]`        | Users for per-user profile settings    |
| `browser_user_config_mode` | `'initial'` | Default mode: managed/initial/disabled |

## Tags

| Tag                  | Scope                       |
| -------------------- | --------------------------- |
| `browser`            | All browser tasks           |
| `browser:install`    | Package installation        |
| `browser:firefox`    | Firefox policy deployment   |
| `browser:chromium`   | Chromium policy deployment  |
| `browser:librewolf`  | LibreWolf policy deployment |
| `browser:brave`      | Brave policy deployment     |
| `browser:configure`  | Per-user profile config     |
| `browser:default`    | Default browser setting     |

## Example Playbook

```yaml
- name: Browser
  hosts: workstations
  tasks:
    - name: Browser | Include browser role
      ansible.builtin.include_role:
        name: marcstraube.desktop.browser
      tags: [browser]
      when: browser_enabled | default(true) | bool
```

## Testing

```bash
cd roles/browser
molecule test
```

- **Driver:** Podman
- **Platforms:** Arch Linux, Debian Trixie, Rocky 9, Rocky 10

## References

- [Firefox](https://www.mozilla.org/firefox/) — Open-source web browser
- [Mozilla Policy Templates](https://mozilla.github.io/policy-templates/) — Reference for `policies.json` keys deployed by this role
- [arkenfox/user.js](https://github.com/arkenfox/user.js) — Hardened Firefox `user.js` template the role's defaults derive from
- [Chromium](https://www.chromium.org/) — Open-source browser project
- [Chromium Enterprise Policy List](https://chromeenterprise.google/policies/) — Reference for Chromium/Brave policy keys
- [LibreWolf](https://librewolf.net/) — Privacy-focused Firefox fork
- [Brave](https://brave.com/) — Privacy-focused Chromium fork
- [Tor Browser](https://www.torproject.org/) — Anonymity-focused Firefox fork
- [Zen Browser](https://zen-browser.app/) — Productivity-focused Firefox fork

## License

MIT

## Author

Marc Straube
