import os

class CopyToClipboardUseCase:
    
    def __init__(self, directory_processor, clipboard_adapter):
        self.directory_processor = directory_processor
        self.clipboard_adapter = clipboard_adapter

    def execute(self, dir_path):
        """
        Existing single-directory use case. 
        Grabs the entire 'dir_path' recursively and copies it.
        """
        tree_lines = self.directory_processor.generate_tree(dir_path)
        file_contents = self.directory_processor.collect_file_contents(dir_path)
        output = '\n'.join(tree_lines) + '\n\n' + '\n'.join(file_contents)
        self.clipboard_adapter.copy(output)
        return 'Directory tree and file contents copied to clipboard.'


class CopyMultiplePathsUseCase:
    """
    NEW use case for multiple files and/or folders at once.
    """

    def __init__(self, directory_processor, clipboard_adapter):
        self.directory_processor = directory_processor
        self.clipboard_adapter = clipboard_adapter

    def execute(self, paths):
        """
        - 'paths' can be a mix of files and directories
        - We create a single big text block from them all.
        """
        combined_text_blocks = []

        for path in paths:
            if os.path.isfile(path):
                # Minimal logic for a single file
                filename = os.path.basename(path)
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                except Exception as e:
                    content = f"<Error reading file: {e}>"
                text_block = (
                    f"----BEGINNING OF {filename}------\n"
                    f"{content}\n"
                    f"----END OF {filename}-------\n"
                )
                combined_text_blocks.append(text_block)
            elif os.path.isdir(path):
                # Reuse directory logic from DirectoryProcessor
                tree_lines = self.directory_processor.generate_tree(path)
                file_contents = self.directory_processor.collect_file_contents(path)
                dir_output = '\n'.join(tree_lines) + '\n\n' + '\n'.join(file_contents)
                combined_text_blocks.append(dir_output)
            else:
                # Not file or folder (e.g., broken link)
                combined_text_blocks.append(f"<Skipping unknown path: {path}>")

        final_output = "\n".join(combined_text_blocks)
        self.clipboard_adapter.copy(final_output)

        return "Selected items copied to clipboard!"
