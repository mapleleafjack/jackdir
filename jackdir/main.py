# jackdir/main.py

import os
import sys
import argparse

from pathspec import PathSpec
import pyperclip

def parse_args():
    parser = argparse.ArgumentParser(description='Copy directory tree and file contents to clipboard')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to process (default: current directory)')
    parser.add_argument('--include-hidden', '-i', action='store_true', help='Include hidden files and directories')
    return parser.parse_args()

def should_exclude(path, is_dir, args, spec, dir_path):
    name = os.path.basename(path)
    if not args.include_hidden and name.startswith('.'):
        return True
    if spec is not None and spec.match_file(os.path.relpath(path, dir_path)):
        return True
    return False

def generate_tree(dir_path, args, spec):
    tree_lines = []
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), True, args, spec, dir_path)]
        files[:] = [f for f in files if not should_exclude(os.path.join(root, f), False, args, spec, dir_path)]
        
        level = os.path.relpath(root, dir_path).count(os.sep)
        indent = '    ' * level
        if root == dir_path:
            tree_lines.append('.')
        else:
            tree_lines.append('{}{}/'.format(indent, os.path.basename(root)))
        
        for f in files:
            tree_lines.append('{}    {}'.format(indent, f))
    return tree_lines

def collect_file_contents(dir_path, args, spec):
    file_contents = []
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), True, args, spec, dir_path)]
        files[:] = [f for f in files if not should_exclude(os.path.join(root, f), False, args, spec, dir_path)]
        
        for f in files:
            file_path = os.path.join(root, f)
            relative_file_path = os.path.relpath(file_path, dir_path)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
            except Exception as e:
                content = '<Error reading file: {}>'.format(e)
            
            file_contents.append('----BEGINNING OF {}------\n{}\n----END OF {}-------\n'.format(
                relative_file_path, content, relative_file_path))
    return file_contents

def main():
    args = parse_args()
    dir_path = os.path.abspath(args.directory)
    
    gitignore_path = os.path.join(dir_path, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        patterns = gitignore_content.splitlines()
        spec = PathSpec.from_lines('gitwildmatch', patterns)
    else:
        spec = None
    
    tree_lines = generate_tree(dir_path, args, spec)
    file_contents = collect_file_contents(dir_path, args, spec)
    
    output = '\n'.join(tree_lines) + '\n\n' + '\n'.join(file_contents)
    
    pyperclip.copy(output)
    print('Directory tree and file contents copied to clipboard.')

if __name__ == '__main__':
    main()
