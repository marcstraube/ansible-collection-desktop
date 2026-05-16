# Changelog

## [2.0.0](https://github.com/marcstraube/ansible-collection-desktop/compare/v1.2.1...v2.0.0) (2026-05-16)


### ⚠ BREAKING CHANGES

* **keepassxc:** switch autostart to XDG and expand ini defaults ([#111](https://github.com/marcstraube/ansible-collection-desktop/issues/111))
* migrate Firefox locked prefs to policies.json Preferences policy ([#104](https://github.com/marcstraube/ansible-collection-desktop/issues/104))
* **wayland_utils:** rename swww to awww and add matugen toggle ([#93](https://github.com/marcstraube/ansible-collection-desktop/issues/93))
* Implement wine 'initial' user_config_mode; flip default to 'initial' ([#60](https://github.com/marcstraube/ansible-collection-desktop/issues/60))
* Implement keepassxc 'initial' user_config_mode; flip default to 'initial' ([#59](https://github.com/marcstraube/ansible-collection-desktop/issues/59))
* Implement starship config; flip shell_user_config_mode default to 'initial' ([#58](https://github.com/marcstraube/ansible-collection-desktop/issues/58))
* Change browser_user_config_mode default to 'initial' ([#55](https://github.com/marcstraube/ansible-collection-desktop/issues/55))
* Use enum-style scope for keepassxc secret service ([#44](https://github.com/marcstraube/ansible-collection-desktop/issues/44))
* Rename boolean toggles to follow naming convention ([#43](https://github.com/marcstraube/ansible-collection-desktop/issues/43))
* Switch shell role default from zsh to bash ([#42](https://github.com/marcstraube/ansible-collection-desktop/issues/42))
* Remove deprecated CLI file manager variables ([#41](https://github.com/marcstraube/ansible-collection-desktop/issues/41))

### Features

* add xdg_user_dirs role for managing XDG user directories ([#107](https://github.com/marcstraube/ansible-collection-desktop/issues/107)) ([bd96200](https://github.com/marcstraube/ansible-collection-desktop/commit/bd962005f526332e75cbf64b37a53e8ab82dd4e1))
* **keepassxc:** switch autostart to XDG and expand ini defaults ([#111](https://github.com/marcstraube/ansible-collection-desktop/issues/111)) ([f4dc595](https://github.com/marcstraube/ansible-collection-desktop/commit/f4dc5957cc0fef938fd290e3fbea37ae1ce24c5e)), closes [#110](https://github.com/marcstraube/ansible-collection-desktop/issues/110) [#46](https://github.com/marcstraube/ansible-collection-desktop/issues/46)
* **office:** add betterbird (AUR) as Thunderbird alternative ([#95](https://github.com/marcstraube/ansible-collection-desktop/issues/95)) ([6663a68](https://github.com/marcstraube/ansible-collection-desktop/commit/6663a68da5809f5e204498a6852b57c21e9ffcbe)), closes [#94](https://github.com/marcstraube/ansible-collection-desktop/issues/94)
* per-user VSCode/VSCodium settings + telemetry opt-out ([#105](https://github.com/marcstraube/ansible-collection-desktop/issues/105)) ([4201640](https://github.com/marcstraube/ansible-collection-desktop/commit/4201640105b1ed08e30b3237af21611a848cc563))
* **playbooks:** Add system_update task file for Arch partial-upgrade safety ([#37](https://github.com/marcstraube/ansible-collection-desktop/issues/37)) ([e41b76f](https://github.com/marcstraube/ansible-collection-desktop/commit/e41b76f31aa919e48c593d80038b30958f2beee1))


### Bug Fixes

* assert multilib repo enabled before installing lib32 packages ([#99](https://github.com/marcstraube/ansible-collection-desktop/issues/99)) ([9b875c2](https://github.com/marcstraube/ansible-collection-desktop/commit/9b875c2941d46712f868a2f0067c4bc007dd1aba))
* **development:** flip cmake/meson/ninja default to true ([#68](https://github.com/marcstraube/ansible-collection-desktop/issues/68)) ([151a60a](https://github.com/marcstraube/ansible-collection-desktop/commit/151a60ad263d5cc0c91112eb88bc3834ccfabe95)), closes [#67](https://github.com/marcstraube/ansible-collection-desktop/issues/67)
* **filemanagers:** handle Rocky 9/10 EPEL packaging gaps ([#71](https://github.com/marcstraube/ansible-collection-desktop/issues/71)) ([099a188](https://github.com/marcstraube/ansible-collection-desktop/commit/099a188b86190c4e6d3947d1b50f816a0f11249d))
* Firefox/LibreWolf profile bootstrap + policies.json valid JSON ([#102](https://github.com/marcstraube/ansible-collection-desktop/issues/102)) ([95502d9](https://github.com/marcstraube/ansible-collection-desktop/commit/95502d918d7c3652f5f5f8d29e603fe99cb58f74))
* **graphics_apps:** include full var set on RedHat ([#80](https://github.com/marcstraube/ansible-collection-desktop/issues/80)) ([fc4fa8d](https://github.com/marcstraube/ansible-collection-desktop/commit/fc4fa8d2a7eec57e6d6448197fa4b0ccc43aa689)), closes [#74](https://github.com/marcstraube/ansible-collection-desktop/issues/74)
* Implement install toggles for documented dev tools; drop development_java_version ([#61](https://github.com/marcstraube/ansible-collection-desktop/issues/61)) ([d279359](https://github.com/marcstraube/ansible-collection-desktop/commit/d2793596659f9f57343b8dd4f3a0a2ede1dfaa6d)), closes [#47](https://github.com/marcstraube/ansible-collection-desktop/issues/47)
* Implement keepassxc 'initial' user_config_mode; flip default to 'initial' ([#59](https://github.com/marcstraube/ansible-collection-desktop/issues/59)) ([c664b25](https://github.com/marcstraube/ansible-collection-desktop/commit/c664b25a66088e245e80f43359bc7cd632608f8a)), closes [#46](https://github.com/marcstraube/ansible-collection-desktop/issues/46)
* Implement wine 'initial' user_config_mode; flip default to 'initial' ([#60](https://github.com/marcstraube/ansible-collection-desktop/issues/60)) ([2f90cff](https://github.com/marcstraube/ansible-collection-desktop/commit/2f90cffa25593bf243fcc685154061a5e9d87e28)), closes [#53](https://github.com/marcstraube/ansible-collection-desktop/issues/53)
* manage browser default via mimeapps.list instead of xdg-settings ([#100](https://github.com/marcstraube/ansible-collection-desktop/issues/100)) ([e7cc578](https://github.com/marcstraube/ansible-collection-desktop/commit/e7cc5783e91572808fd620d18a42084ad9a2b064))
* **playbooks:** include wine role in desktop_workstation task file ([#86](https://github.com/marcstraube/ansible-collection-desktop/issues/86)) ([9025b8b](https://github.com/marcstraube/ansible-collection-desktop/commit/9025b8bdb53ab0114189cd629690ec370cc73226))
* **plymouth:** Add --all argument to HSM sign script call ([#33](https://github.com/marcstraube/ansible-collection-desktop/issues/33)) ([c0a3b44](https://github.com/marcstraube/ansible-collection-desktop/commit/c0a3b4445751267260d89df695a575b4fa32e7c4))
* **shell:** wire shell_starship_shells — append starship init per shell ([#64](https://github.com/marcstraube/ansible-collection-desktop/issues/64)) ([b5e7a6e](https://github.com/marcstraube/ansible-collection-desktop/commit/b5e7a6ecab32980dcb7824820ed05c166ca9f2a8))
* **terminal:** export $TERMINAL to login shells via /etc/profile.d ([#91](https://github.com/marcstraube/ansible-collection-desktop/issues/91)) ([b846886](https://github.com/marcstraube/ansible-collection-desktop/commit/b846886609c057cf624f6ac0a7103d2ce719af64))
* **tuxedo:** detect kernels from pacman DB, support multi-kernel ([#85](https://github.com/marcstraube/ansible-collection-desktop/issues/85)) ([f818f82](https://github.com/marcstraube/ansible-collection-desktop/commit/f818f82a2bf46a9ce1d8a0ef119222edf54ce317))
* **tuxedo:** drop state management for sleep.target-driven tccd-sleep ([#89](https://github.com/marcstraube/ansible-collection-desktop/issues/89)) ([a5ed0e1](https://github.com/marcstraube/ansible-collection-desktop/commit/a5ed0e18eb8611a693a331fabbc2615fc749647f))
* unblock v2.0.0 CI matrix across desktop roles ([#70](https://github.com/marcstraube/ansible-collection-desktop/issues/70)) ([731e737](https://github.com/marcstraube/ansible-collection-desktop/commit/731e737be80567cf8e0dedeb8ce6d5a5a31ed4ed)), closes [#72](https://github.com/marcstraube/ansible-collection-desktop/issues/72) [#73](https://github.com/marcstraube/ansible-collection-desktop/issues/73) [#75](https://github.com/marcstraube/ansible-collection-desktop/issues/75) [#76](https://github.com/marcstraube/ansible-collection-desktop/issues/76) [#77](https://github.com/marcstraube/ansible-collection-desktop/issues/77) [#78](https://github.com/marcstraube/ansible-collection-desktop/issues/78) [#79](https://github.com/marcstraube/ansible-collection-desktop/issues/79)


### Code Refactoring

* **browser:** extract Firefox-family per-user profile bootstrap into shared helper ([#113](https://github.com/marcstraube/ansible-collection-desktop/issues/113)) ([fe21579](https://github.com/marcstraube/ansible-collection-desktop/commit/fe215790f54a686b58ee84e150eba08d70ed2f47)), closes [#112](https://github.com/marcstraube/ansible-collection-desktop/issues/112)
* Change browser_user_config_mode default to 'initial' ([#55](https://github.com/marcstraube/ansible-collection-desktop/issues/55)) ([4664fa9](https://github.com/marcstraube/ansible-collection-desktop/commit/4664fa9fbccc706716893fef9fc75e1753e8f86a)), closes [#52](https://github.com/marcstraube/ansible-collection-desktop/issues/52)
* Implement LXQt variant; drop unused desktop_environment_default and _cursor_size ([#57](https://github.com/marcstraube/ansible-collection-desktop/issues/57)) ([ce65f88](https://github.com/marcstraube/ansible-collection-desktop/commit/ce65f882324595e673de5ed3bbccea44b309ba24)), closes [#49](https://github.com/marcstraube/ansible-collection-desktop/issues/49)
* Implement starship config; flip shell_user_config_mode default to 'initial' ([#58](https://github.com/marcstraube/ansible-collection-desktop/issues/58)) ([d9fe67a](https://github.com/marcstraube/ansible-collection-desktop/commit/d9fe67a1a791cd9ef6372e7f9e8b05394a59a9cf)), closes [#51](https://github.com/marcstraube/ansible-collection-desktop/issues/51)
* migrate Firefox locked prefs to policies.json Preferences policy ([#104](https://github.com/marcstraube/ansible-collection-desktop/issues/104)) ([74dabed](https://github.com/marcstraube/ansible-collection-desktop/commit/74dabed485290d5432f104e21cfc163d459809e3))
* **playbooks:** Extract desktop_workstation tasks + align with common patterns ([#35](https://github.com/marcstraube/ansible-collection-desktop/issues/35)) ([66dd1d0](https://github.com/marcstraube/ansible-collection-desktop/commit/66dd1d00b2a16cb82ec53732e9eb22cb4febe098))
* Remove deprecated CLI file manager variables ([#41](https://github.com/marcstraube/ansible-collection-desktop/issues/41)) ([e8caedf](https://github.com/marcstraube/ansible-collection-desktop/commit/e8caedf91fd41c0c45f612757e9ed9bc1c42f309))
* Remove unused SDDM and LightDM theme variables ([#54](https://github.com/marcstraube/ansible-collection-desktop/issues/54)) ([efa3e32](https://github.com/marcstraube/ansible-collection-desktop/commit/efa3e32d2df70d0c43ef39322e22b6907eac8a0e)), closes [#50](https://github.com/marcstraube/ansible-collection-desktop/issues/50)
* Remove unused terminal config vars; implement terminal_default ([#56](https://github.com/marcstraube/ansible-collection-desktop/issues/56)) ([351376b](https://github.com/marcstraube/ansible-collection-desktop/commit/351376b3f4819e244235644d08e1f67c6acfa111)), closes [#48](https://github.com/marcstraube/ansible-collection-desktop/issues/48)
* Rename boolean toggles to follow naming convention ([#43](https://github.com/marcstraube/ansible-collection-desktop/issues/43)) ([0cdb186](https://github.com/marcstraube/ansible-collection-desktop/commit/0cdb1863e4602a81950c320ee46d58ffc0bab929))
* Switch shell role default from zsh to bash ([#42](https://github.com/marcstraube/ansible-collection-desktop/issues/42)) ([28916be](https://github.com/marcstraube/ansible-collection-desktop/commit/28916befa02ec32ddf70dab1f5882dedebe50949))
* Use enum-style scope for keepassxc secret service ([#44](https://github.com/marcstraube/ansible-collection-desktop/issues/44)) ([4cf4673](https://github.com/marcstraube/ansible-collection-desktop/commit/4cf4673077c2be087a4ca71c5390bbd7abd861bc))
* **wayland_utils:** rename swww to awww and add matugen toggle ([#93](https://github.com/marcstraube/ansible-collection-desktop/issues/93)) ([37e0dd5](https://github.com/marcstraube/ansible-collection-desktop/commit/37e0dd5300b981d2ee8bb63065139f67f59b2c40))


### Documentation

* add References sections to roles touched in v2.0.0 prep ([#65](https://github.com/marcstraube/ansible-collection-desktop/issues/65)) ([ad5927d](https://github.com/marcstraube/ansible-collection-desktop/commit/ad5927d8d3da0fc213d6152c69d06855cf55bcfd)), closes [#66](https://github.com/marcstraube/ansible-collection-desktop/issues/66)
* **keepassxc:** document FdoSecrets group assignment as manual setup ([#97](https://github.com/marcstraube/ansible-collection-desktop/issues/97)) ([e892191](https://github.com/marcstraube/ansible-collection-desktop/commit/e8921915c86a7b2e390f43045f867879a335a31c)), closes [#96](https://github.com/marcstraube/ansible-collection-desktop/issues/96)
* **readme:** list xdg_user_dirs role and fix markdown lint ([#108](https://github.com/marcstraube/ansible-collection-desktop/issues/108)) ([61438b6](https://github.com/marcstraube/ansible-collection-desktop/commit/61438b608f921694ea86aa0447b4240031aef024))

## [1.2.1](https://github.com/marcstraube/ansible-collection-desktop/compare/v1.2.0...v1.2.1) (2026-04-20)


### Bug Fixes

* **playbooks:** Correct role gate conditions in desktop_workstation ([#28](https://github.com/marcstraube/ansible-collection-desktop/issues/28)) ([e553514](https://github.com/marcstraube/ansible-collection-desktop/commit/e553514208944b678fcbe9a4deade50c3eaafad7))


### Documentation

* **shell:** Add deprecation notice for zsh defaults ([#27](https://github.com/marcstraube/ansible-collection-desktop/issues/27)) ([f8bc54c](https://github.com/marcstraube/ansible-collection-desktop/commit/f8bc54c89855f744c4e47b55e564395e0fcad464))

## [1.2.0](https://github.com/marcstraube/ansible-collection-desktop/compare/v1.1.0...v1.2.0) (2026-04-19)


### Features

* Add network retry logic to transient tasks ([#23](https://github.com/marcstraube/ansible-collection-desktop/issues/23)) ([0866567](https://github.com/marcstraube/ansible-collection-desktop/commit/08665677c06554ef92e083045d5ecf64e36b7a62))


### Bug Fixes

* **multimedia:** Disable abandoned packages by default ([#21](https://github.com/marcstraube/ansible-collection-desktop/issues/21)) ([b15fe86](https://github.com/marcstraube/ansible-collection-desktop/commit/b15fe863d9477add368affcc769135262d2926a3))


### Miscellaneous

* **filemanagers:** Deprecate CLI file managers ([#18](https://github.com/marcstraube/ansible-collection-desktop/issues/18)) ([dbbe857](https://github.com/marcstraube/ansible-collection-desktop/commit/dbbe8579fcb30ecf618221ce90004b0df49aab3e))

## [1.1.0](https://github.com/marcstraube/ansible-collection-desktop/compare/v1.0.0...v1.1.0) (2026-04-16)


### Features

* **shell:** Add Oh My Zsh framework support ([#7](https://github.com/marcstraube/ansible-collection-desktop/issues/7)) ([68b3f9a](https://github.com/marcstraube/ansible-collection-desktop/commit/68b3f9aef21ce143ba70213dd2fbdc6389be62dc))


### Bug Fixes

* Rename gaming_wine to wine_enabled in example playbooks ([23fd81b](https://github.com/marcstraube/ansible-collection-desktop/commit/23fd81b955a197cac08330bfcf281d1020d24e75))
* Use explicit generic updater for galaxy.yml in release-please ([c3167b1](https://github.com/marcstraube/ansible-collection-desktop/commit/c3167b163b1e22094b7d5e439b79d6e0a684b8b6))

## v1.0.0 (2026-04-15)

Initial release of the marcstraube.desktop collection.

### Included Roles (27)

ai, bluetooth, browser, cad, communication, desktop_environment,
development, display_manager, downloads, elgato, filemanagers, gaming,
graphics_apps, imaging, keepassxc, multimedia, office, pipewire,
plymouth, remote_access, security_apps, shell, system_apps, tabletop,
terminal, tuxedo, wayland_utils, wine
