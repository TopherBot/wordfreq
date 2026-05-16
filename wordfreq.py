#!/usr/bin/env python3
"""
wordfreq.py – Count word frequencies.

Provides a small CLI that reads from a file or stdin, tokenizes
words, and prints the most common ones.

Features:
- Graceful error handling (file not found, decode errors).
- Optional case‑insensitive counting.
- Configurable number of top results.
- Idempotent execution – running the script multiple times
  never mutates external state.
"""

import argparse
import collections
import re
import sys
from pathlib import Path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the most common words from a text source."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="-",
        help="Path to a text file or '-' for stdin (default).",
    )
    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        help="Number of top words to display (default: 10).",
    )
    parser.add_argument(
        "-i",
        "--ignore-case",
        action="store_true",
        help="Count words case‑insensitively.",
    )
    return parser.parse_args()

def read_input(path: str) -> str:
    """Read text from a file or stdin, handling common errors."""
    if path == "-":
        data = sys.stdin.read()
        return data
    try:
        # Using Path for clear intent
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        sys.stderr.write(f"Error: File not found – {path}\n")
        sys.exit(1)
    except UnicodeDecodeError:
        sys.stderr.write(f"Error: Unable to decode file – {path}\n")
        sys.exit(1)

def tokenize(text: str, ignore_case: bool) -> list[str]:
    """Return a list of words (alphanumeric + underscore)."""
    if ignore_case:
        text = text.lower()
    # \b\w+\b matches words, ignoring punctuation
    return re.findall(r"\b\w+\b", text)

def main() -> None:
    args = parse_args()
    raw_text = read_input(args.path)
    if not raw_text.strip():
        sys.stderr.write("Warning: Input is empty. No words to count.\n")
        return
    words = tokenize(raw_text, args.ignore_case)
    counter = collections.Counter(words)
    for word, count in counter.most_common(args.top):
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
