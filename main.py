#!/usr/bin/env python3
"""Laugh Track — validate one crypto-trading joke line and publish it.

Reads entry.txt next to this script, validates it (exactly one line,
non-empty, 1-160 characters), and writes it unchanged to /output/entry.txt.
Pure Python standard library only.
"""

import os
import sys

MAX_CHARS = 160


def load_joke(path):
    """Read the joke file and return its single line, stripped of newline."""
    with open(path, "r", encoding="utf-8") as handle:
        content = handle.read()
    lines = content.splitlines()
    if len(lines) != 1:
        raise ValueError(
            "entry.txt must contain exactly one line, found %d" % len(lines)
        )
    return lines[0]


def validate_no_extra_whitespace(joke):
    """Reject leading/trailing whitespace so the published line is clean."""
    if joke != joke.strip():
        raise ValueError("joke must not have leading or trailing whitespace")
    return joke


def validate_joke(joke):
    """Check the joke is a non-empty single line within the length limit."""
    validate_no_extra_whitespace(joke)
    if not joke.strip():
        raise ValueError("joke must not be empty")
    if len(joke) > MAX_CHARS:
        raise ValueError(
            "joke is %d characters, over the %d limit" % (len(joke), MAX_CHARS)
        )
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    return joke


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.txt")
    joke = validate_joke(load_joke(source))
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(joke + "\n")
    print("OK: joke is %d chars" % len(joke))
    print(joke)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(1)
