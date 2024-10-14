from jackdir.adapters.clipboard_adapter import ClipboardAdapter
from unittest import mock

class TestClipboardAdapter:
    @mock.patch('pyperclip.copy')
    def test_copy(self, mock_copy):
        adapter = ClipboardAdapter()
        test_text = 'Test content'
        adapter.copy(test_text)
        mock_copy.assert_called_once_with(test_text)
