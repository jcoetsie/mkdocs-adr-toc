import os
import unittest
from unittest.mock import MagicMock, patch
from adr_toc_plugin import ADRTOCPlugin

class TestADRTOCPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = ADRTOCPlugin()
        self.plugin.config = {
            'toc_file': 'index.md',
            'placeholder': '<!-- ADR_SUMMARY_PLACEHOLDER -->',
            'adr_path': 'decisions'
        }

    @patch('adr_toc_plugin.os.listdir')
    @patch('adr_toc_plugin.open', new_callable=unittest.mock.mock_open, read_data='''# Title
status: "Accepted"
date: "2023-01-01"
deciders: ["Alice", "Bob"]
''')
    def test_on_page_markdown(self, mock_open, mock_listdir):
        mock_listdir.return_value = ['001-decision.md']
        page = MagicMock()
        page.file.src_path = 'index.md'
        config = {'docs_dir': '/docs'}
        files = []

        result = self.plugin.on_page_markdown('<!-- ADR_SUMMARY_PLACEHOLDER -->', page, config, files)
        
        self.assertIn('| 001 | [Title](decisions/001-decision.md) | Accepted | 2023-01-01 | Alice, Bob |', result)

    @patch('adr_toc_plugin.os.listdir')
    @patch('adr_toc_plugin.open', new_callable=unittest.mock.mock_open, read_data='''# Title
status: "Accepted"
date: "2023-01-01"
deciders: ["Alice", "Bob"]
''')
    def test_on_page_markdown_no_placeholder(self, mock_open, mock_listdir):
        mock_listdir.return_value = ['001-decision.md']
        page = MagicMock()
        page.file.src_path = 'index.md'
        config = {'docs_dir': '/docs'}
        files = []

        result = self.plugin.on_page_markdown('Some other content', page, config, files)
        
        self.assertNotIn('| 001 | [Title](decisions/001-decision.md) | Accepted | 2023-01-01 | Alice, Bob |', result)

if __name__ == '__main__':
    unittest.main()
