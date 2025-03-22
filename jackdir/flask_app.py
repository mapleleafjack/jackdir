# jackdir/flask_app.py

from flask import Flask, render_template, request, jsonify
import os

from jackdir.entities.directory_processor import DirectoryProcessor
from jackdir.adapters.clipboard_adapter import ClipboardAdapter
from jackdir.use_cases.copy_to_clipboard import CopyMultiplePathsUseCase
from jackdir.main import load_gitignore_spec

app = Flask(__name__)

@app.route("/")
def home():
    # Renders our "index.html" template (see below)
    return render_template("index.html")

@app.route("/api/tree", methods=["POST"])
def api_tree():
    """
    Build a nested JSON tree for the entire directory. 
    Expects JSON body: { "directory": "...", "include_hidden": bool }
    Returns structure like:
    {
      "name": "rootdir",
      "path": "/absolute/path",
      "type": "directory",
      "children": [
        {
          "name": "subdir",
          "path": "/absolute/path/subdir",
          "type": "directory",
          "children": [...]
        },
        {
          "name": "file.txt",
          "path": "/absolute/path/file.txt",
          "type": "file"
        }
      ]
    }
    """
    data = request.get_json(force=True)
    directory = os.path.abspath(data.get("directory", "."))
    include_hidden = data.get("include_hidden", False)

    if not os.path.isdir(directory):
        return jsonify({
            "error": f"Invalid directory: {directory}",
            "tree": None
        })

    # Load .gitignore, if applicable
    spec = load_gitignore_spec(directory)
    dp = DirectoryProcessor(include_hidden=include_hidden, spec=spec)

    # Recursively build the tree
    def build_tree(path):
        name = os.path.basename(path) or path  # if path is '/', name might be empty
        node = {
            "name": name,
            "path": path,
            "type": "directory",  # assume directory until proven otherwise
            "children": []
        }
        if not os.path.isdir(path):
            # It's a file
            node["type"] = "file"
            node["children"] = []
            return node
        # It's a directory - gather children
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            # Could not list directory
            return {
                "name": name,
                "path": path,
                "type": "directory",
                "children": []
            }

        for entry_name in entries:
            full_child = os.path.join(path, entry_name)
            is_dir = os.path.isdir(full_child)
            # Use DirectoryProcessor to decide if we skip it
            if dp.should_exclude(full_child, is_dir, directory):
                continue
            node["children"].append(build_tree(full_child))

        return node

    tree = build_tree(directory)

    return jsonify({
        "error": None,
        "tree": tree
    })

@app.route("/api/copy_selected", methods=["POST"])
def api_copy_selected():
    """
    Expects JSON: { "selected_paths": [...], "include_hidden": bool }
    Uses CopyMultiplePathsUseCase to copy all selected items.
    """
    data = request.get_json(force=True)
    selected_paths = data.get("selected_paths", [])
    include_hidden = data.get("include_hidden", False)

    if not selected_paths:
        return jsonify({
            "error": "No items selected.",
            "message": None
        })

    # We'll guess the first path's parent is the 'root' for .gitignore,
    # or you can pass directory from the client if you like.
    base_dir = os.path.dirname(selected_paths[0]) if selected_paths else '.'
    spec = load_gitignore_spec(base_dir)
    dp = DirectoryProcessor(include_hidden=include_hidden, spec=spec)
    clipboard = ClipboardAdapter()

    use_case = CopyMultiplePathsUseCase(dp, clipboard)
    msg = use_case.execute(selected_paths)

    return jsonify({
        "error": None,
        "message": msg
    })

def run_flask_app():
    app.run(debug=True)

if __name__ == "__main__":
    run_flask_app()
