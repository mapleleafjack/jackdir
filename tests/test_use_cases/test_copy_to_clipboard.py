from jackdir.use_cases.copy_to_clipboard import CopyToClipboardUseCase
from unittest import mock

class TestCopyToClipboardUseCase:
    def test_execute(self):
        # Mock DirectoryProcessor
        mock_directory_processor = mock.Mock()
        mock_directory_processor.generate_tree.return_value = ['.', '    file.txt']
        mock_directory_processor.collect_file_contents.return_value = [
            '----BEGINNING OF file.txt------\nContent\n----END OF file.txt-------\n'
        ]

        # Mock ClipboardAdapter
        mock_clipboard_adapter = mock.Mock()

        use_case = CopyToClipboardUseCase(mock_directory_processor, mock_clipboard_adapter)
        result = use_case.execute('/fake/path')

        expected_output = '.\n    file.txt\n\n----BEGINNING OF file.txt------\nContent\n----END OF file.txt-------\n'
        mock_clipboard_adapter.copy.assert_called_once_with(expected_output)
        assert result == 'Directory tree and file contents copied to clipboard.'
