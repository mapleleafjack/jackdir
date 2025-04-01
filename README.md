# jackdir

A handy command-line tool to grab your directory's structure and all its file contents, and copy them straight to your clipboard.
Ever needed to quickly share the layout and content of a project directory? jackdir makes it simple.
Need a code review from ChatGPT? Just run the command and paste!

## How to install
Make sure you have Python 3 installed. Then, just run:

```bash
pip install .
```

If you're running on MacOS and/or you want to install the package globally, you can use pipx

```bash
pipx install .
```

## Running the frontend:
```bash
jackdir-flask
```

## CLI usage:
Open your terminal and type:

```bash
jackdir [directory] [--include-hidden]
```

- directory: The folder you want to process (if you skip this, it uses your current directory).

## Running Tests:

If you want to run tests

```bash
pytest tests/
```

## Want to Help?

I welcome contributions! If you have ideas or find issues, feel free to open an issue or submit a pull request.

## Special thanks to
Daniel, who gave me the initial idea!
