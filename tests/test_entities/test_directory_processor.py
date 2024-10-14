import os
import tempfile
import shutil
from jackdir.entities.directory_processor import DirectoryProcessor
from pathspec import PathSpec

class TestDirectoryProcessor:
    def setup_method(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        # Create sample files and directories
        os.makedirs(os.path.join(self.test_dir, 'subdir'))
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write('Content of file1')
        with open(os.path.join(self.test_dir, 'subdir', 'file2.txt'), 'w') as f:
            f.write('Content of file2')
        # Hidden file
        with open(os.path.join(self.test_dir, '.hidden_file'), 'w') as f:
            f.write('Hidden content')

    def teardown_method(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_generate_tree_without_hidden(self):
        dp = DirectoryProcessor(include_hidden=False)
        tree = dp.generate_tree(self.test_dir)
        expected_tree = [
            '.',
            '    file1.txt',
            '    subdir/',
            '        file2.txt'
        ]
        assert tree == expected_tree

    def test_generate_tree_with_hidden(self):
        dp = DirectoryProcessor(include_hidden=True)
        tree = dp.generate_tree(self.test_dir)
        expected_tree = [
            '.',
            '    .hidden_file',
            '    file1.txt',
            '    subdir/',
            '        file2.txt'
        ]
        assert tree == expected_tree


    def test_collect_file_contents_without_hidden(self):
        dp = DirectoryProcessor(include_hidden=False)
        contents = dp.collect_file_contents(self.test_dir)
        expected_contents = [
            '----BEGINNING OF file1.txt------\nContent of file1\n----END OF file1.txt-------\n',
            '----BEGINNING OF subdir/file2.txt------\nContent of file2\n----END OF subdir/file2.txt-------\n'
        ]
        assert contents == expected_contents

    def test_collect_file_contents_with_hidden(self):
        dp = DirectoryProcessor(include_hidden=True)
        contents = dp.collect_file_contents(self.test_dir)
        expected_contents = [
            '----BEGINNING OF .hidden_file------\nHidden content\n----END OF .hidden_file-------\n',
            '----BEGINNING OF file1.txt------\nContent of file1\n----END OF file1.txt-------\n',
            '----BEGINNING OF subdir/file2.txt------\nContent of file2\n----END OF subdir/file2.txt-------\n'
        ]
        assert contents == expected_contents

    def test_should_exclude_with_gitignore(self):
        # Create a .gitignore file
        gitignore_path = os.path.join(self.test_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write('file1.txt\n')
        # Load gitignore patterns
        with open(gitignore_path, 'r') as f:
            patterns = f.read().splitlines()
        spec = PathSpec.from_lines('gitwildmatch', patterns)

        dp = DirectoryProcessor(include_hidden=False, spec=spec)
        tree = dp.generate_tree(self.test_dir)
        expected_tree = [
            '.',
            '    subdir/',
            '        file2.txt'
        ]
        assert tree == expected_tree

