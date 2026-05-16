# wordfreq

A tiny command‑line utility that counts word frequencies in a text file (or standard input) and prints a sorted list. It works with Python 3.8+.

## Usage

```sh
python3 wordfreq.py path/to/file.txt
# or read from stdin
cat file.txt | python3 wordfreq.py
```

## Options

- `-n, --top N` – Show only the top N words (default: 10).
- `-i, --ignore-case` – Count words case‑insensitively.

The script never mutates external state, making it safe to run repeatedly.
