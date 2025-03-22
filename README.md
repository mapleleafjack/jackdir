# jackdir

A handy command-line tool to grab your directory's structure and all its file contents, and copy them straight to your clipboard.
Ever needed to quickly share the layout and content of a project directory? jackdir makes it simple.
Need a code review from ChatGPT? Just run the command and paste!

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

## Running the frontend:
```bash
jackdir-flask
```

and in another terminal 
```bash
cd client && npm start
```

## Running Tests:

If you want to run tests

```bash
pytest tests/
```

## Want to Help?

I welcome contributions! If you have ideas or find issues, feel free to open an issue or submit a pull request.

## Special thanks to
Daniel, who gave me the initial idea!
