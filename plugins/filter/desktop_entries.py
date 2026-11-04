"""Filters of the marcstraube.desktop.desktop_entries role.

desktop_entries_exec
    Prefix an Exec= value with ``env NAME=value ...`` (variables sorted by
    name). An empty mapping returns the value unchanged.

desktop_entries_override
    Apply environment, set and append changes to the text of a desktop entry
    and return the changed text. The edits work on lines and know the group
    each line belongs to:

    * environment: every Exec= line of every group ([Desktop Entry] and the
      [Desktop Action ...] groups) gets the env prefix.
    * set_keys: keys of the [Desktop Entry] group. An existing key is
      replaced, a missing one is added at the end of the group. Only the exact
      key matches: Name does not touch Name[de].
    * append_keys: list keys (;-separated) of the [Desktop Entry] group.
      Values not yet in the list are appended in the given order; a missing
      key is created. The list always ends with a semicolon.

    set_keys applies before append_keys. Other lines (comments, blank lines,
    other groups, localized keys) stay as they are.

The role validates names and values with assert tasks before it calls these
filters; the filters only convert booleans to the desktop entry form
(true/false) and reject an entry without a [Desktop Entry] group when a key
has to be set or appended.
"""

import re

from ansible.errors import AnsibleFilterError

MAIN_GROUP = 'Desktop Entry'

# A ; that is not escaped as \;
LIST_SEPARATOR = re.compile(r'(?<!\\);')


def _text(value):
    """Return a value as text; booleans in the desktop entry form."""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return str(value)


def _env_prefix(environment):
    if not environment:
        return ''
    pairs = ('%s=%s' % (name, _text(environment[name])) for name in sorted(environment))
    return 'env ' + ' '.join(pairs) + ' '


def desktop_entries_exec(value, environment=None):
    """Prefix an Exec= value with env NAME=value for every variable."""
    return _env_prefix(environment or {}) + _text(value)


def _split_key(line):
    """Return (key, value) of a key=value line, or (None, None)."""
    stripped = line.strip()
    if not stripped or stripped.startswith('#') or '=' not in stripped:
        return None, None
    key, _, value = stripped.partition('=')
    return key.strip(), value.strip()


def _append_list(current, values):
    items = [item for item in LIST_SEPARATOR.split(current or '') if item]
    for value in values:
        value = _text(value)
        if value not in items:
            items.append(value)
    return ';'.join(items) + ';'


def desktop_entries_override(content, environment=None, set_keys=None, append_keys=None):
    """Return the desktop entry text with the requested changes applied."""
    environment = environment or {}
    set_keys = dict((key, _text(value)) for key, value in (set_keys or {}).items())
    append_keys = dict(append_keys or {})
    prefix = _env_prefix(environment)

    lines = content.splitlines()
    groups = [line.strip()[1:-1] for line in lines
              if line.strip().startswith('[') and line.strip().endswith(']')]
    if (set_keys or append_keys) and MAIN_GROUP not in groups:
        raise AnsibleFilterError(
            'desktop_entries_override: the desktop entry has no [%s] group' % MAIN_GROUP)

    output = []
    group = None
    seen = set()

    def close_main_group():
        # Missing keys go after the last line of the group that is not blank,
        # so the blank line before the next group stays in place.
        missing = []
        for key, value in set_keys.items():
            if key not in seen and key not in append_keys:
                missing.append((key, value))
        for key, values in append_keys.items():
            if key not in seen:
                missing.append((key, _append_list(set_keys.get(key, ''), values)))
        missing = ['%s=%s%s' % (key, prefix if key == 'Exec' else '', value)
                   for key, value in missing]
        position = len(output)
        while position > 0 and not output[position - 1].strip():
            position -= 1
        output[position:position] = missing

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('[') and stripped.endswith(']'):
            if group == MAIN_GROUP:
                close_main_group()
            group = stripped[1:-1]
            output.append(line)
            continue

        key, value = _split_key(line)
        if group is None or key is None:
            output.append(line)
            continue

        if group == MAIN_GROUP and (key in set_keys or key in append_keys):
            seen.add(key)
            if key in set_keys:
                value = set_keys[key]
            if key in append_keys:
                value = _append_list(value, append_keys[key])
            line = '%s=%s' % (key, value)

        if key == 'Exec' and prefix:
            line = 'Exec=' + prefix + value

        output.append(line)

    if group == MAIN_GROUP:
        close_main_group()

    return '\n'.join(output)


class FilterModule(object):
    """Desktop entry filters."""

    def filters(self):
        return {
            'desktop_entries_exec': desktop_entries_exec,
            'desktop_entries_override': desktop_entries_override,
        }
