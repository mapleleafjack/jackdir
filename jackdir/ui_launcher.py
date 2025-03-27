import os
import subprocess
import sys
import shutil
import tempfile
from threading import Thread
from pathlib import Path
from pkg_resources import resource_filename

def run_flask():
    """Start the Flask backend with proper environment."""
    env = os.environ.copy()
    env['FLASK_APP'] = 'jackdir.flask_app'
    # run on port 6666
    env['FLASK_RUN_PORT'] = '6789'
    
    subprocess.run([sys.executable, "-m", "flask", "run"], env=env)

def run_react():
    """Start the React frontend using a temporary, writable copy of the packaged client folder."""
    # Locate the client folder within the installed package
    packaged_client_path = Path(resource_filename('jackdir', 'client'))
    print(f"[DEBUG] Packaged client path: {packaged_client_path}")
    if not packaged_client_path.exists():
        raise FileNotFoundError(f"Client directory not found at: {packaged_client_path}")
    
    # Create a temporary copy of the client folder
    temp_client_dir = Path(tempfile.mkdtemp(prefix="jackdir_client_"))
    print(f"[DEBUG] Temporary client directory: {temp_client_dir}")
    shutil.copytree(packaged_client_path, temp_client_dir / "client", dirs_exist_ok=True)
    client_path = temp_client_dir / "client"
    
    # Change to the temporary client folder
    os.chdir(client_path)
    
    # Check if npm is available
    npm_path = shutil.which('npm')
    if npm_path is None:
        raise EnvironmentError("npm command not found in PATH. Please ensure npm is installed and in PATH.")
    print(f"[DEBUG] Using npm at: {npm_path}")
    
    # Remove any existing node_modules (in case something was copied over)
    node_modules_path = client_path / "node_modules"
    if node_modules_path.exists():
        shutil.rmtree(node_modules_path)
    
    # Install dependencies
    print("[DEBUG] Running 'npm install'...")
    subprocess.run([npm_path, 'install'], check=True)
    
    print("[DEBUG] Starting React development server with 'npm start'...")
    proc = subprocess.Popen([npm_path, 'start'])
    return proc

def main():
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    react_proc = run_react()
    
    try:
        react_proc.wait()
    except KeyboardInterrupt:
        print("Terminating React process...")
        react_proc.terminate()
        react_proc.wait()
        print("React process terminated.")

if __name__ == "__main__":
    main()
