# marcstraube.desktop.browser

Install and configure web browsers with enterprise policies and hardening.

## Description

Installs and configures web browsers with system-wide enterprise policies for
extension management, privacy hardening, and telemetry control. Supports
Firefox, LibreWolf, Chromium, Brave, Google Chrome, Tor Browser, and Zen
Browser.

Browser extensions are managed via policies (force-installed, user-installable,
or blocked). Firefox/LibreWolf system-wide locked preferences go through the
Mozilla `Preferences` policy inside `policies.json` (whitelist-bound, see
upstream `Policies.sys.mjs`). Per-user, user-overridable hardening lives in
`<profile>/user.js`.

LibreWolf, Brave, Tor Browser, and Zen Browser are installed from AUR on
Arch Linux. Tor Browser is available via `torbrowser-launcher` on Debian.
Chromium on Rocky Linux requires EPEL.

Google Chrome is available on every platform: from AUR (`google-chrome`) on
Arch Linux, and from Google's own vendor package on Debian/EL. On Debian/EL
the vendor package's post-install script installs and owns Google's apt/yum
repository and signing key, so Chrome updates through the normal system
upgrade path (the role installs the package directly rather than adding a
second, conflicting repository entry). Chrome is opt-in
(`browser_chrome_enabled: false`) and shares the Chromium extension and
policy mechanism.

## Requirements

- ansible-core >= 2.17
- `community.general` collection (pacman module)
- `kewlfft.aur` collection (Arch Linux AUR packages)
- Rocky Linux requires EPEL to be enabled for Chromium.
  EPEL is managed by the `marcstraube.common.package_management` role.

## Supported Platforms

| Platform       | Firefox | LibreWolf | Tor | Zen | Chromium | Brave | Chrome |
| -------------- | ------- | --------- | --- | --- | -------- | ----- | ------ |
| Arch Linux     | yes     | AUR       | AUR | AUR | yes      | AUR   | AUR    |
| Debian Trixie  | ESR     | no        | yes | no  | yes      | no    | repo   |
| EL 9           | yes     | no        | no  | no  | EPEL     | no    | repo   |
| EL 10          | yes     | no        | no  | no  | EPEL     | no    | repo   |

## Role Variables

### Role Control

| Variable          | Default | Description         |
| ----------------- | ------- | ------------------- |
| `browser_enabled` | `true`  | Enable/disable role |

### Browsers to Install

| Variable                     | Default     | Description                   |
| ---------------------------- | ----------- | ----------------------------- |
| `browser_firefox_enabled`    | `true`      | Install Firefox               |
| `browser_librewolf_enabled`  | `false`     | Install LibreWolf (Arch only) |
| `browser_tor_enabled`        | `false`     | Install Tor Browser           |
| `browser_zen_enabled`        | `false`     | Install Zen Browser (Arch)    |
| `browser_chromium_enabled`   | `true`      | Install Chromium              |
| `browser_brave_enabled`      | `false`     | Install Brave (Arch only)     |
| `browser_chrome_enabled`     | `false`     | Install Google Chrome         |
| `browser_default`            | `'firefox'` | Default http/https handler    |

### Firefox Options

| Variable                              | Default | Description                           |
| ------------------------------------- | ------- | ------------------------------------- |
| `browser_firefox_policies_enabled`    | `true`  | Deploy policies.json                  |
| `browser_firefox_user_js_enabled`     | `true`  | Deploy per-user user.js               |
| `browser_firefox_i18n`                | `''`    | Language pack code (empty = none)     |
| `browser_firefox_extensions`          | `{...}` | Extensions with install modes         |
| `browser_firefox_extensions_optional` | `{}`    | Optional extensions (user-selectable) |
| `browser_firefox_preferences`         | `{}`    | User-overridable prefs → `user.js`    |
| `browser_firefox_policy_settings`     | `{...}` | policies.json settings (incl. locked) |

### LibreWolf Options

| Variable                                    | Default | Description                      |
| ------------------------------------------- | ------- | -------------------------------- |
| `browser_librewolf_policies_enabled`        | `true`  | Deploy policies.json             |
| `browser_librewolf_user_js_enabled`         | `true`  | Deploy per-user user.js          |
| `browser_librewolf_extensions`              | `{...}` | Extensions (defaults to Firefox) |
| `browser_librewolf_preferences`             | `{}`    | Additional preferences           |
| `browser_librewolf_disable_telemetry`       | `true`  | Disable telemetry                |
| `browser_librewolf_disable_pocket`          | `true`  | Disable Pocket                   |
| `browser_librewolf_disable_firefox_studies` | `true`  | Disable Firefox studies          |
| `browser_librewolf_homepage`                | `''`    | Homepage URL (empty = default)   |
| `browser_librewolf_no_default_bookmarks`    | `true`  | Remove default bookmarks         |
| `browser_librewolf_offer_to_save_logins`    | `false` | Offer to save logins             |
| `browser_librewolf_password_manager`        | `false` | Built-in password manager        |

### Chromium Options

| Variable                                      | Default     | Description                       |
| --------------------------------------------- | ----------- | --------------------------------- |
| `browser_chromium_policies_enabled`           | `true`      | Deploy policies                   |
| `browser_chromium_wayland_gestures_enabled`   | `true`      | Wayland gesture hook (Arch only)  |
| `browser_chromium_flags_enabled`              | `false`     | Per-user chromium-flags.conf      |
| `browser_chromium_flags`                      | `[]`        | Launch switches (one per line)    |
| `browser_chromium_extensions`                 | `{...}`     | Extensions with install modes     |
| `browser_chromium_extensions_optional`        | `{}`        | Optional extensions (merged)      |
| `browser_chromium_policy_settings`            | `{...}`     | Additional policy settings        |

### Brave Options

| Variable                              | Default     | Description                       |
| ------------------------------------- | ----------- | --------------------------------- |
| `browser_brave_policies_enabled`      | `true`      | Deploy policies                   |
| `browser_brave_extensions`            | `{...}`     | Extensions (defaults to Chromium) |
| `browser_brave_extensions_optional`   | `{}`        | Optional extensions (merged)      |
| `browser_brave_homepage`              | `''`        | Homepage URL (empty = default)    |
| `browser_brave_signin`                | `0`         | Sign-in: 0=off, 1=on, 2=required  |
| `browser_brave_sync_disabled`         | `true`      | Disable Brave Sync                |
| `browser_brave_metrics`               | `false`     | Metrics reporting                 |
| `browser_brave_safe_browsing`         | `true`      | Safe Browsing                     |
| `browser_brave_password_manager`      | `false`     | Built-in password manager         |
| `browser_brave_autofill_address`      | `false`     | Autofill address forms            |
| `browser_brave_autofill_credit_card`  | `false`     | Autofill credit card forms        |

### Chrome Options

| Variable                              | Default     | Description                       |
| ------------------------------------- | ----------- | --------------------------------- |
| `browser_chrome_policies_enabled`     | `true`      | Deploy policies                   |
| `browser_chrome_flags_enabled`        | `false`     | Per-user chrome-flags.conf (Arch) |
| `browser_chrome_flags`                | `[]`        | Launch switches (one per line)    |
| `browser_chrome_extensions`           | `{...}`     | Extensions (defaults to Chromium) |
| `browser_chrome_extensions_optional`  | `{}`        | Optional extensions (merged)      |
| `browser_chrome_homepage`             | `''`        | Homepage URL (empty = default)    |
| `browser_chrome_signin`               | `0`         | Sign-in: 0=off, 1=on, 2=required  |
| `browser_chrome_sync_disabled`        | `true`      | Disable Chrome Sync               |
| `browser_chrome_metrics`              | `false`     | Metrics reporting                 |
| `browser_chrome_safe_browsing`        | `true`      | Safe Browsing                     |
| `browser_chrome_password_manager`     | `false`     | Built-in password manager         |
| `browser_chrome_autofill_address`     | `false`     | Autofill address forms            |
| `browser_chrome_autofill_credit_card` | `false`     | Autofill credit card forms        |

Google Chrome uses the Chromium extension and policy mechanism. The launch
switches in `browser_chrome_flags` are only read by Arch's `google-chrome`
AUR launcher (`~/.config/chrome-flags.conf`); Google's own launcher on
Debian/EL ignores them.

### Extension Control

| Variable                          | Default     | Description                 |
| --------------------------------- | ----------- | --------------------------- |
| `browser_extension_default_mode`  | `'blocked'` | Default: allowed or blocked |

### User Configuration

| Variable                   | Default     | Description                                  |
| -------------------------- | ----------- | -------------------------------------------- |
| `browser_users`            | `[]`        | Users for per-user profile settings          |
| `browser_user_config_mode` | `'initial'` | Default mode: managed/initial/seed/disabled  |

`browser_default` is applied per-user via `~/.config/mimeapps.list`
(sections `[Default Applications]`, keys `x-scheme-handler/http`
and `x-scheme-handler/https`). Previously this used `xdg-settings`,
which silently failed without a graphical session. The value must
match the `.desktop` basename of an installed browser, without the
suffix (e.g. `firefox`, `librewolf`, `chromium`, `brave-browser`).
Set to an empty string to skip handler management. Other entries
in `mimeapps.list` are preserved on each run. The same
`managed`/`initial`/`seed`/`disabled` mode that governs per-user profile
config applies here too — `initial` deploys only on newly created
users, leaving subsequent manual changes intact.

`browser_chromium_flags` (`~/.config/chromium-flags.conf`) and the
per-user `user.js` are whole-file deploys and additionally honour `seed`
mode: the file is written only when absent (`force: false`) and never
overwritten afterwards. Use `seed` to roll a new config out to an
existing user once and then leave it under the user's control — unlike
`initial`, which is gated on user creation and so never reaches existing
users. `mimeapps.list` manages individual handler keys rather than a
whole file, so it treats `seed` like `initial`.

### Firefox / LibreWolf preferences — locked vs. user-overridable

Two mechanisms, two variables, distinct semantics:

- **`browser_firefox_policy_settings.Preferences`** (and `_librewolf_…`) deploy via `policies.json` as
  **system-wide locked** prefs. Only the
  [Mozilla whitelist of allowed prefixes](https://github.com/mozilla/gecko-dev/blob/master/browser/components/enterprisepolicies/Policies.sys.mjs)
  is honored — non-whitelisted entries are silently ignored by Mozilla. Format:

  ```yaml
  browser_firefox_policy_settings:
    Preferences:
      network.prefetch-next:
        Value: false
        Status: locked
  ```

- **`browser_firefox_preferences`** (and `_librewolf_…`) deploy as `user_pref()` in `<profile>/user.js` —
  **per-user, overridable in `about:config`** until the next managed-mode run reconciles. Use this for
  prefs that aren't on the policy whitelist, or for defaults the user should be able to change.

The role's defaults intentionally leave `browser_firefox_preferences` empty: every soft-hardening pref
worth defaulting is either already covered by another policy (e.g. `DisableTelemetry` covers all
telemetry prefs) or by recent Firefox built-in defaults. The two non-trivial leftovers
(`network.prefetch-next`, `network.dns.disablePrefetch`) live in `Preferences` policy.

### Firefox / LibreWolf profile bootstrap

For Firefox and LibreWolf, the role writes the profile directory,
`profiles.ini`, and `user.js` directly (Mozilla's `-CreateProfile`
CLI is a silent no-op in non-interactive contexts). To make the
bootstrapped profile actually take effect on first launch, the role
also writes a per-install `[Install<hash>]` section in
`profiles.ini` — without it, modern Firefox (>= 67) ignores
`[Profile0].Default=1` and auto-creates its own random-prefix
profile, locking the install to that one.

The install hash is `CityHash64` of the UTF-16-LE encoded install
directory path (see Mozilla source `commonupdatedir.cpp::GetInstallHash`).
Pre-computed hashes for the standard distro install paths are
hardcoded in `vars/{Archlinux,Debian,RedHat}.yml`
(`__browser_firefox_install_hash`, `__browser_librewolf_install_hash`).

To compute the hash for a custom install path:

```bash
go run github.com/bradenhilton/mozillainstallhash/cmd/mozhash@latest <path>
# e.g. mozhash /opt/firefox  → custom 16-char uppercase hex
```

If the install hash is left empty, the profile is still written but
the browser will not pick it up as default — fall back to detecting
the random-prefix profile the browser creates on first launch.

## Tags

| Tag                  | Scope                       |
| -------------------- | --------------------------- |
| `browser`            | All browser tasks           |
| `browser:install`    | Package installation        |
| `browser:firefox`    | Firefox policy deployment   |
| `browser:librewolf`  | LibreWolf policy deployment |
| `browser:chromium`   | Chromium policy deployment  |
| `browser:brave`      | Brave policy deployment     |
| `browser:chrome`     | Chrome policy deployment    |
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
- [Mozilla Policy Templates](https://mozilla.github.io/policy-templates/) —
  Reference for `policies.json` keys deployed by this role
- [arkenfox/user.js](https://github.com/arkenfox/user.js) —
  Hardened Firefox `user.js` template the role's defaults derive from
- [LibreWolf](https://librewolf.net/) — Privacy-focused Firefox fork
- [Tor Browser](https://www.torproject.org/) — Anonymity-focused Firefox fork
- [Zen Browser](https://zen-browser.app/) — Productivity-focused Firefox fork
- [Chromium](https://www.chromium.org/) — Open-source browser project
- [Chromium Enterprise Policy List](https://chromeenterprise.google/policies/) —
  Reference for Chromium/Brave/Chrome policy keys
- [Brave](https://brave.com/) — Privacy-focused Chromium fork
- [Google Chrome](https://www.google.com/chrome/) — Chromium-based browser
- [Linux Software Repositories](https://www.google.com/linuxrepositories/) —
  Google's apt/yum repository the vendor package configures for updates

## License

MIT

## Author

Marc Straube
