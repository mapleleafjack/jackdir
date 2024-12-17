# jackdir

Asking ChatGPT about your code? Boom, done.

`jackdir` grabs your entire project — files, folders, the whole thing — packs it up, and copies it straight to your clipboard. 
Just paste it into your favorite LLM and let the magic happen. 

Debug, brainstorm, or flex your masterpiece with zero hassle.

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
