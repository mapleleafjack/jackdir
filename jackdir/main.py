import os
import argparse
from pathspec import PathSpec

from jackdir.entities.directory_processor import DirectoryProcessor
from jackdir.use_cases.copy_to_clipboard import CopyToClipboardUseCase
from jackdir.adapters.clipboard_adapter import ClipboardAdapter

def parse_args():
    parser = argparse.ArgumentParser(description='Copy directory tree and file contents to clipboard')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to process (default: current directory)')
    parser.add_argument('--include-hidden', '-i', action='store_true', help='Include hidden files and directories')
    return parser.parse_args()

def load_gitignore_spec(dir_path):
    gitignore_path = os.path.join(dir_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        patterns = gitignore_content.splitlines()
        return PathSpec.from_lines('gitwildmatch', patterns)
    return None

def main():
    args = parse_args()
    dir_path = os.path.abspath(args.directory)
    spec = load_gitignore_spec(dir_path)

    directory_processor = DirectoryProcessor(args.include_hidden, spec)
    clipboard_adapter = ClipboardAdapter()
    copy_to_clipboard_use_case = CopyToClipboardUseCase(directory_processor, clipboard_adapter)
    
    result = copy_to_clipboard_use_case.execute(dir_path)
    print(result)

if __name__ == '__main__':
    main()
