import os
from pathspec import PathSpec

class DirectoryProcessor:
    
    def __init__(self, include_hidden=False, spec=None):
        self.include_hidden = include_hidden
        
        # Default patterns to exclude common files/directories
        default_patterns = [
            'node_modules/',
            '__pycache__/',
            '*.py[co]',
            '*.pyd',
            '.env',
            'venv/',
            'env/',
            '.venv/',
            'dist/',
            'build/',
            '*.egg-info/',
            'package-lock.json',
            'yarn.lock',
            'pnpm-lock.yaml',
            'venv/'
        ]
        default_spec = PathSpec.from_lines('gitwildmatch', default_patterns)
        
        # Combine with provided spec if available
        if spec is not None:
            provided_patterns = [p.pattern for p in spec.patterns]
            combined_patterns = default_patterns + provided_patterns
            self.spec = PathSpec.from_lines('gitwildmatch', combined_patterns)
        else:
            self.spec = default_spec

    def should_exclude(self, path, is_dir, dir_path):
        name = os.path.basename(path)
        if not self.include_hidden and name.startswith('.'):
            return True
        
        # Get relative path and normalize to POSIX-style
        rel_path = os.path.relpath(path, dir_path).replace(os.sep, '/')
        
        # Append trailing slash for directories to match gitignore patterns
        if is_dir:
            rel_path += '/'
        
        return self.spec.match_file(rel_path)


    def generate_tree(self, dir_path):
        tree_lines = []
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = sorted([
                d for d in dirs if not self.should_exclude(os.path.join(root, d), True, dir_path)
            ])
            files[:] = sorted([
                f for f in files if not self.should_exclude(os.path.join(root, f), False, dir_path)
            ])
            
            # Calculate the relative path and level
            rel_path = os.path.relpath(root, dir_path)
            if root == dir_path:
                level = 0
                indent = ''
                tree_lines.append('.')
            else:
                level = rel_path.count(os.sep) + 1  # Increment level for subdirectories
                indent = '    ' * level
                tree_lines.append(f'{indent}{os.path.basename(root)}/')
            
            sub_indent = '    ' * (level + 1)
            for f in files:
                tree_lines.append(f'{sub_indent}{f}')
        return tree_lines

    def collect_file_contents(self, dir_path):
        file_contents_list = []
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = sorted([
                d for d in dirs if not self.should_exclude(os.path.join(root, d), True, dir_path)
            ])
            files[:] = sorted([
                f for f in files if not self.should_exclude(os.path.join(root, f), False, dir_path)
            ])
            
            for f in files:
                file_path = os.path.join(root, f)
                relative_file_path = os.path.relpath(file_path, dir_path)
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                except Exception as e:
                    content = f'<Error reading file: {e}>'
                
                # Collect as tuples for sorting
                file_contents_list.append((relative_file_path, content))
        
        # Sort the file contents by relative file path
        file_contents_list.sort(key=lambda x: x[0])
        
        # Build the final file_contents list
        file_contents = []
        for relative_file_path, content in file_contents_list:
            file_contents.append(
                f'----BEGINNING OF {relative_file_path}------\n{content}\n----END OF {relative_file_path}-------\n'
            )
        return file_contents


