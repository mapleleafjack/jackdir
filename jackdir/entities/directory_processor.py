import os

class DirectoryProcessor:
    
    def __init__(self, include_hidden=False, spec=None):
        self.include_hidden = include_hidden
        self.spec = spec

    def should_exclude(self, path, is_dir, dir_path):
        name = os.path.basename(path)
        if not self.include_hidden and name.startswith('.'):
            return True
        if self.spec and self.spec.match_file(os.path.relpath(path, dir_path)):
            return True
        return False

    def generate_tree(self, dir_path):
        tree_lines = []
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d), True, dir_path)]
            files[:] = [f for f in files if not self.should_exclude(os.path.join(root, f), False, dir_path)]
            
            level = os.path.relpath(root, dir_path).count(os.sep)
            indent = '    ' * level
            if root == dir_path:
                tree_lines.append('.')
            else:
                tree_lines.append(f'{indent}{os.path.basename(root)}/')
            
            for f in files:
                tree_lines.append(f'{indent}    {f}')
        return tree_lines

    def collect_file_contents(self, dir_path):
        file_contents = []
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d), True, dir_path)]
            files[:] = [f for f in files if not self.should_exclude(os.path.join(root, f), False, dir_path)]
            
            for f in files:
                file_path = os.path.join(root, f)
                relative_file_path = os.path.relpath(file_path, dir_path)
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                except Exception as e:
                    content = f'<Error reading file: {e}>'
                
                file_contents.append(f'----BEGINNING OF {relative_file_path}------\n{content}\n----END OF {relative_file_path}-------\n')
        return file_contents
