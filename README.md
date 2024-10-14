# jackdir

A handy command-line tool to grab your directory's structure and all its file contents, and copy them straight to your clipboard.
Ever needed to quickly share the layout and content of a project directory? jackdir makes it simple.

## Key Features:

- Easy Directory Snapshot: Captures the folder structure and files.
- Content Collection: Gathers the contents of all files in the directory.
- Respects .gitignore: Automatically skips files and folders you've marked to ignore.
- Optional Hidden Files: Choose whether to include hidden files and directories

## How to install

Make sure you have Python 3 installed. Then, just run:

```bash
pip install .
```

## How to Use:
Open your terminal and type:

```bash
jackdir [directory] [--include-hidden]
```

- directory: The folder you want to process (if you skip this, it uses your current directory).
- --include-hidden or -i: Add this if you want to include hidden files and folders.
Examples:

To process your current directory, excluding hidden stuff:

```bash
jackdir
```

To process a specific folder and include everything, even hidden files:

```bash
jackdir /path/to/directory -i
```

## Running Tests:

If you want to run tests to make sure everything's working, type:

```bash
pytest tests/
```

## Want to Help?

I welcome contributions! If you have ideas or find issues, feel free to open an issue or submit a pull request.