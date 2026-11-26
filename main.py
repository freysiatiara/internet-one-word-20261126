"""Write the chosen word for The Internet in One Word to the output file.

Reads entry.txt next to this script, validates it is a single word of
1-30 characters, and writes it verbatim to the output path.
Standard library only.
"""

import os
import sys


def resolve_output_path():
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for variable in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(variable)
        if directory:
            return os.path.join(directory, "entry.txt")
    return "/output/entry.txt"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, "entry.txt")
    with open(source_path, "r", encoding="utf-8") as handle:
        word = handle.read()
    if not word or len(word) > 30:
        raise SystemExit("entry must be 1-30 characters")
    if word != word.strip() or any(ch.isspace() for ch in word):
        raise SystemExit("entry must be exactly one word with no whitespace")
    if not word.isalpha():
        raise SystemExit("entry must contain letters only")
    if not word.isprintable():
        raise SystemExit("entry must be printable text")
    output_path = resolve_output_path()
    parent = os.path.dirname(os.path.abspath(output_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(word)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(output_path, 0o644)
    if (os.stat(output_path).st_mode & 0o777) != 0o644:
        raise SystemExit("output file mode is not 0644")
    with open(output_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != word:
        raise SystemExit("round-trip read-back mismatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
