import pyperclip

class ClipboardAdapter:
    
    def copy(self, text):
        pyperclip.copy(text)
