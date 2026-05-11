# office

Install office applications and document tools.

## Requirements

- `kewlfft.aur` collection (for AUR packages on Arch Linux)

## Supported Platforms

| Platform                    | Notes                                                                                                            |
|-----------------------------|------------------------------------------------------------------------------------------------------------------|
| Arch Linux                  | Native packages + AUR                                                                                            |
| Debian Trixie               | Official repo packages                                                                                           |
| EL 9 (Rocky, Alma, RHEL)    | EPEL packages — gnome-contacts, foliate, gscan2pdf not available                                                 |
| EL 10 (Rocky, Alma, RHEL)   | EPEL packages — calibre, foliate, texstudio, gnome-calendar, gnome-contacts not available; evince → GNOME Papers |

Other distributions in the same os_family (EndeavourOS, Manjaro, Ubuntu, Mint,
Fedora) should work but are not actively tested. Use distro-specific vars
overrides if needed.

## Role Variables

### Role Control

| Variable         | Default | Description            |
|------------------|---------|------------------------|
| `office_enabled` | `true`  | Enable the office role |

### Office Suites

| Variable                           | Default | Description                            |
|------------------------------------|---------|----------------------------------------|
| `office_libreoffice_enabled`       | `true`  | Enable LibreOffice installation        |
| `office_libreoffice_fresh_enabled` | `true`  | Use LibreOffice Fresh instead of Still |
| `office_libreoffice_i18n`          | `'de'`  | Language pack for LibreOffice          |
| `office_onlyoffice_enabled`        | `false` | Enable OnlyOffice Desktop (AUR only)   |
| `office_wps_enabled`               | `false` | Enable WPS Office (AUR only)           |

### PDF Tools

| Variable                   | Default    | Description                                 |
|----------------------------|------------|---------------------------------------------|
| `office_pdf_viewer`        | `'evince'` | PDF viewer (evince, okular, zathura, mupdf) |
| `office_pdf_tools_enabled` | `true`     | Enable PDF command line tools               |

### Email Clients

| Variable                     | Default | Description               |
|------------------------------|---------|---------------------------|
| `office_thunderbird_enabled` | `false` | Enable Thunderbird        |
| `office_thunderbird_i18n`    | `'de'`  | Thunderbird language pack |
| `office_evolution_enabled`   | `false` | Enable Evolution          |

### Calendar / PIM

| Variable                        | Default | Description           |
|---------------------------------|---------|-----------------------|
| `office_gnome_calendar_enabled` | `false` | Enable GNOME Calendar |
| `office_gnome_contacts_enabled` | `false` | Enable GNOME Contacts |

### Note Taking

| Variable                    | Default | Description                  |
|-----------------------------|---------|------------------------------|
| `office_obsidian_enabled`   | `false` | Enable Obsidian (AUR only)   |
| `office_logseq_enabled`     | `false` | Enable Logseq (AUR only)     |
| `office_joplin_enabled`     | `false` | Enable Joplin (AUR only)     |
| `office_simplenote_enabled` | `false` | Enable Simplenote (AUR only) |

### Document Tools

| Variable                   | Default          | Description                  |
|----------------------------|------------------|------------------------------|
| `office_typora_enabled`    | `false`          | Enable Typora (AUR only)     |
| `office_texstudio_enabled` | `false`          | Enable TeXstudio             |
| `office_ocr_enabled`       | `false`          | Enable OCR tools (tesseract) |
| `office_ocr_languages`     | `['eng', 'deu']` | OCR language data packages   |

### Scanning

| Variable                     | Default | Description        |
|------------------------------|---------|--------------------|
| `office_simple_scan_enabled` | `false` | Enable Simple Scan |
| `office_gscan2pdf_enabled`   | `false` | Enable gscan2pdf   |

### Ebook

| Variable                 | Default | Description                 |
|--------------------------|---------|-----------------------------|
| `office_calibre_enabled` | `false` | Enable Calibre              |
| `office_foliate_enabled` | `false` | Enable Foliate ebook reader |

### Misc

| Variable                  | Default | Description                    |
|---------------------------|---------|--------------------------------|
| `office_hunspell_enabled` | `true`  | Enable Hunspell spell checking |
| `office_fonts_enabled`    | `true`  | Enable office fonts            |

## Tags

| Tag              | Description               |
|------------------|---------------------------|
| `office`         | All office tasks          |
| `office:install` | Package installation only |

## Example Playbook

```yaml
- hosts: workstations
  become: true
  tasks:
    - name: Include office role
      ansible.builtin.include_role:
        name: marcstraube.desktop.office
      tags:
        - office
```

## Testing

```bash
cd collections/ansible_collections/marcstraube/desktop/roles/office
molecule test -p office-archlinux
```

## License

MIT

## Author

Marc Straube
