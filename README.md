# jackdir

A CLI tool to copy directory tree and file contents to the clipboard.

## Installation

```bash
pip install .
```

## Usage

```bash
jackdir [directory] [--include-hidden]
```

- directory: The directory to process (default: current directory).
- --include-hidden or -i: Include hidden files and directories.

## Example

```bash
jackdir . -i
```