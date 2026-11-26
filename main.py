"""Museum placard for a stapler, written as an ancient artifact.

The program takes one catalogue line — a stapler recast as a ritual
binding tool of the Accounts Department — and publishes it to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output/entry.txt``).

Every gate rule is checked before anything is written: the line must
be UTF-8 text of 1-180 characters, a single line, not blank, and free
of control characters, byte-order marks, line/paragraph separators,
and any other invisible formatting. The publish step is atomic — a
temp file staged inside the output directory, flushed to disk,
swapped into place, and read back for a byte-exact confirmation.
"""

import os
import sys
import unicodedata

PLACARD_LINE = (
    "Stapler, c. 2019, steel and plastic. Ritual binding tool of the "
    "Accounts Department; unused since spring 2021, when the last jam "
    "was declared an omen."
)

SHORTEST = 1
LONGEST = 180

NEVER_ALLOWED = ("\ufeff", "\u2028", "\u2029")


def _is_control_code(ch):
    """C1 controls, surrogates, and Cc/Cf category characters."""
    code = ord(ch)
    if 0x0080 <= code <= 0x009F:
        return True
    if 0xD800 <= code <= 0xDFFF:
        return True
    return unicodedata.category(ch) in ("Cc", "Cf")


def _is_invisible_format(ch):
    """BOM, line/paragraph separators, and other zero-width marks."""
    if ch in NEVER_ALLOWED:
        return True
    return unicodedata.category(ch) == "Cf"


def _is_separator(ch):
    """Whitespace that is not a plain space (tabs, exotic spaces)."""
    return ch.isspace() and ch != " "


def _is_banned_glyph(ch):
    """True when a character must never reach the placard text."""
    return _is_control_code(ch) or _is_invisible_format(ch) or _is_separator(ch)


def _check_shape(text):
    """Reject non-strings, blank text, multi-line text, bad lengths."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry is empty or whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not SHORTEST <= len(text) <= LONGEST:
        raise ValueError(
            "entry is %d characters; gate requires %d-%d"
            % (len(text), SHORTEST, LONGEST)
        )


def _check_characters(text):
    """Reject, one by one, every character the gate forbids."""
    for ch in text:
        if _is_banned_glyph(ch):
            raise ValueError("forbidden character U+%04X in entry" % ord(ch))


def _check_utf8_roundtrip(text):
    """Confirm the text encodes as UTF-8 (raises otherwise)."""
    text.encode("utf-8")


def validate_placard(text):
    """Run every gate check on the entry. Raises ValueError."""
    _check_shape(text)
    _check_characters(text)
    _check_utf8_roundtrip(text)
    return True


def resolve_output_dir():
    """Locate the output directory from the environment."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def _stage_bytes(out_dir, data):
    """Write the bytes to a temp file inside the output directory.

    Staging must stay INSIDE the output dir: /tmp fails with EXDEV
    on bind-mounted output paths, and os.replace must stay on one
    filesystem. The temp file is fsynced and chmodded before the swap.
    """
    staging = os.path.join(out_dir, ".entry.txt.tmp")
    try:
        os.unlink(staging)
    except FileNotFoundError:
        pass  # no stale temp from an earlier interrupted run
    with open(staging, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(staging, 0o644)
    return staging


def _swap_into_place(out_dir, staging):
    """Atomically replace entry.txt with the staged file."""
    target = os.path.join(out_dir, "entry.txt")
    os.replace(staging, target)
    os.chmod(target, 0o644)
    return target


def _confirm_written(target, data):
    """Read the file back: bytes on disk must match exactly."""
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != data:
        raise RuntimeError("read-back mismatch after writing entry.txt")


def publish_placard(text):
    """Validate, write, and verify the placard in the output dir."""
    validate_placard(text)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    data = text.encode("utf-8")
    staging = _stage_bytes(out_dir, data)
    target = _swap_into_place(out_dir, staging)
    _confirm_written(target, data)
    return target


def main():
    try:
        target = publish_placard(PLACARD_LINE)
    except (ValueError, OSError, RuntimeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (target, len(PLACARD_LINE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
