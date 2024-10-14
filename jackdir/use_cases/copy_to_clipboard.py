class CopyToClipboardUseCase:
    
    def __init__(self, directory_processor, clipboard_adapter):
        self.directory_processor = directory_processor
        self.clipboard_adapter = clipboard_adapter

    def execute(self, dir_path):
        tree_lines = self.directory_processor.generate_tree(dir_path)
        file_contents = self.directory_processor.collect_file_contents(dir_path)
        output = '\n'.join(tree_lines) + '\n\n' + '\n'.join(file_contents)
        self.clipboard_adapter.copy(output)
        return 'Directory tree and file contents copied to clipboard.'
