from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from flask_cors import CORS  # Import Flask-CORS
from jackdir.entities.directory_processor import DirectoryProcessor
from jackdir.adapters.clipboard_adapter import ClipboardAdapter
from jackdir.use_cases.copy_to_clipboard import CopyMultiplePathsUseCase
from jackdir.main import load_gitignore_spec

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

app.static_folder = '../client/build/static'

@app.route("/api/tree", methods=["POST"])
def api_tree():
    """
    Build a nested JSON tree for the entire directory.
    Expects JSON body: { "directory": "...", "include_hidden": bool, "respect_gitignore": bool }
    """
    data = request.get_json(force=True)
    directory = os.path.abspath(data.get("directory", "."))
    include_hidden = data.get("include_hidden", False)
    respect_gitignore = data.get("respect_gitignore", True)

    if not os.path.isdir(directory):
        return jsonify({
            "error": f"Invalid directory: {directory}",
            "tree": None
        })

    # Load .gitignore spec only if requested
    spec = load_gitignore_spec(directory) if respect_gitignore else None
    dp = DirectoryProcessor(include_hidden=include_hidden, spec=spec)

    def build_tree(path):
        name = os.path.basename(path) or path  # if path is '/', name might be empty
        node = {
            "name": name,
            "path": path,
            "type": "directory",  # assume directory until proven otherwise
            "children": []
        }
        if not os.path.isdir(path):
            node["type"] = "file"
            node["children"] = []
            return node
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return {
                "name": name,
                "path": path,
                "type": "directory",
                "children": []
            }
        for entry_name in entries:
            full_child = os.path.join(path, entry_name)
            is_dir = os.path.isdir(full_child)
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
    Expects JSON: { "selected_paths": [...], "include_hidden": bool, "respect_gitignore": bool }
    Uses CopyMultiplePathsUseCase to copy all selected items.
    """
    data = request.get_json(force=True)
    selected_paths = data.get("selected_paths", [])
    include_hidden = data.get("include_hidden", False)
    respect_gitignore = data.get("respect_gitignore", True)

    if not selected_paths:
        return jsonify({
            "error": "No items selected.",
            "message": None
        })

    # We'll guess the first path's parent is the 'root' for .gitignore,
    # or you can pass directory from the client if you like.
    base_dir = os.path.dirname(selected_paths[0]) if selected_paths else '.'
    spec = load_gitignore_spec(base_dir) if respect_gitignore else None
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
