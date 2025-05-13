import json
import logging
from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
from jackdir.entities.directory_processor import DirectoryProcessor
from jackdir.adapters.clipboard_adapter import ClipboardAdapter
from jackdir.use_cases.copy_to_clipboard import CopyMultiplePathsUseCase
from jackdir.main import load_gitignore_spec
from openai import OpenAI

app = Flask(__name__, static_folder='client/build')
CORS(app) 

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


def build_tree(path, dp):
    """
    Recursively build a tree (as a Python dict) for the given path.
    """
    name = os.path.basename(path) or path
    node = {
        "name": name,
        "path": path,
        "type": "directory" if os.path.isdir(path) else "file",
        "children": []
    }
    if not os.path.isdir(path):
        return node
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return node
    for entry in entries:
        full_child = os.path.join(path, entry)
        is_dir = os.path.isdir(full_child)
        if dp.should_exclude(full_child, is_dir, os.path.dirname(path)):
            continue
        node["children"].append(build_tree(full_child, dp))
    return node


@app.route("/api/tree", methods=["POST"])
def api_tree():
    """
    Build a nested JSON tree for the entire directory.
    Expects JSON body: { "directory": "...", "include_hidden": bool, "respect_gitignore": bool }
    """
    print("Received request for directory tree")
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

    tree = build_tree(directory, dp)

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

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Extended endpoint for chat that processes selected paths (files or directories)
    similar to the copy_selected endpoint. It appends structural context as well as full 
    file contents for any selected files to the prompt.
    
    Expects JSON with keys:
      - prompt: The user's chat prompt.
      - api_key: API key for OpenAI.
      - model: Model to use (default: "gpt-4o").
      - selected_paths: A list of paths (files and/or directories) to process.
      - include_hidden (optional): whether to include hidden files.
      - respect_gitignore (optional): whether to apply the .gitignore rules.
    """
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    api_key = data.get("api_key", None)
    model = data.get("model", "gpt-4o")
    selected_paths = data.get("selected_paths", [])
    include_hidden = data.get("include_hidden", False)
    respect_gitignore = data.get("respect_gitignore", True)

    extra_context = ""
    if selected_paths:
        base_dir = os.path.dirname(selected_paths[0]) if selected_paths else '.'
        spec = load_gitignore_spec(base_dir) if respect_gitignore else None
        dp = DirectoryProcessor(include_hidden=include_hidden, spec=spec)
        context_sections = []
        for path in selected_paths:
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                context_sections.append(f"[Error] Path does not exist: {abs_path}")
            elif os.path.isfile(abs_path):
                try:
                    with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                        file_content = f.read()
                    section = (
                        f"\n--- Content of File: {abs_path} ---\n"
                        f"{file_content}\n"
                        "-----------------------------------------"
                    )
                    context_sections.append(section)
                except Exception as e:
                    context_sections.append(f"[Error] Could not read file: {abs_path}. Exception: {str(e)}")
            elif os.path.isdir(abs_path):
                tree_representation = build_tree(abs_path, dp)
                # Convert the tree to a pretty JSON string for context
                section = (
                    f"\n--- Directory Structure for: {abs_path} ---\n"
                    f"{json.dumps(tree_representation, indent=2)}\n"
                    "-----------------------------------------"
                )
                context_sections.append(section)
        # Join all context sections into one extra context string.
        extra_context = "\n".join(context_sections)
        # Append the extra context to the chat prompt.
        prompt += "\n\n--- File/Directory Context ---\n" + extra_context

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions="You are a coding assistant that talks like a pirate.",
            input=prompt,
        )
        logging.info(response)
        return jsonify({
            "error": None,
            "response": response.output_text
        })
    except Exception as e:
        logging.exception("Error during chat processing")
        return jsonify({
            "error": str(e),
            "response": None
        }), 500


def run_flask_app():
    # Disable debugger pin and reloader for daemon thread compatibility
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['FLASK_RUN_PORT'] = '6789'

    # Set static folder to React build directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.join(current_dir, 'client', 'build')
    app.static_folder = static_path
    
    # Logging to verify static folder path
    logging.basicConfig(level=logging.INFO)
    app.logger.info(f"Serving static files from: {app.static_folder}")
    if not os.path.exists(app.static_folder):
        app.logger.error("Static folder does not exist!")
    else:
        app.logger.info(f"Static folder contents: {os.listdir(app.static_folder)}")
    
    app.run(port=6789, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_flask_app()
