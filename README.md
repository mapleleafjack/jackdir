# jackdir

Ever needed to quickly share the layout and content of a project directory? jackdir makes it simple.
Asking chatGPT about your code? Nothing simpler!


## How to install

Make sure you have Python 3 installed. Then, just run:

```bash
pip install .
```

If you're running on MacOS and/or you want to install the package globally, you can use pipx

```bash
pipx install .
```

## How to Use:
Open your terminal and type:

```bash
jackdir [directory] [--include-hidden]
```

- directory: The folder you want to process (if you skip this, it uses your current directory).
- --include-hidden or -i: Add this if you want to include hidden files and folders.

## Running Tests:

If you want to run tests

```bash
pytest tests/
```

## Want to Help?

I welcome contributions! If you have ideas or find issues, feel free to open an issue or submit a pull request.