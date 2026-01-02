import unittest

import blocks


class TestBlocks(unittest.TestCase):

    def test_markdown_to_blocks_single_block(self):
        markdown = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        result = blocks.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_multiple_blocks(self):
        markdown = """This is the first paragraph.

This is the second paragraph.

This is the third paragraph."""
        expected = [
            "This is the first paragraph.",
            "This is the second paragraph.",
            "This is the third paragraph."
        ]
        result = blocks.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_with_leading_trailing_whitespace(self):
        markdown = """   This paragraph has leading spaces.   

    This paragraph also has spaces.    """
        expected = [
            "This paragraph has leading spaces.",
            "This paragraph also has spaces."
        ]
        result = blocks.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_multiple_newlines(self):
        markdown = """First paragraph.



Second paragraph after multiple newlines."""
        expected = [
            "First paragraph.",
            "Second paragraph after multiple newlines."
        ]
        result = blocks.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        expected = []
        result = blocks.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n   \n   "
        expected = []
        result = blocks.markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
