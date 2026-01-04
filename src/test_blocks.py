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
    
    def test_block_to_block_type_paragraph(self):
        block = "This is a regular paragraph with some text."
        expected = blocks.BlockType.PARAGRAPH
        result = blocks.block_to_block_type(block)
        self.assertEqual(result, expected)
    
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        expected = blocks.BlockType.HEADING
        result = blocks.block_to_block_type(block)
        self.assertEqual(result, expected)
    
    def test_block_to_block_type_code(self):
        block = "```\nprint('hello world')\n```"
        expected = blocks.BlockType.CODE
        result = blocks.block_to_block_type(block)
        self.assertEqual(result, expected)
    
    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> spanning multiple lines"
        expected = blocks.BlockType.QUOTE
        result = blocks.block_to_block_type(block)
        self.assertEqual(result, expected)
    
    def test_block_to_block_type_unordered_list(self):
        block = "* First item\n* Second item\n* Third item"
        expected = blocks.BlockType.UNORDERED_LIST
        result = blocks.block_to_block_type(block)
        self.assertEqual(result, expected)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        expected = blocks.BlockType.ORDERED_LIST
        result = blocks.block_to_block_type(block)
        self.assertEqual(result, expected)
    
    def test_markdown_to_html_node_paragraph(self):
        markdown = "This is a paragraph."
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
    
    def test_markdown_to_html_node_heading(self):
        markdown = "# This is a heading"
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[0].children[0].value, "This is a heading")
    
    def test_markdown_to_html_node_code(self):
        markdown = "```\nprint('hello')\n```"
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "pre")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].tag, "code")
        self.assertEqual(result.children[0].children[0].value, "print('hello')")
    
    def test_markdown_to_html_node_quote(self):
        markdown = "> This is a quote\n> Second line"
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "blockquote")
        self.assertEqual(result.children[0].children[0].value, "This is a quote\nSecond line")
    
    def test_markdown_to_html_node_unordered_list(self):
        markdown = "* First item\n* Second item"
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "ul")
        self.assertEqual(len(result.children[0].children), 2)
        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].children[0].value, "First item")
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(result.children[0].children[1].children[0].value, "Second item")
    
    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. First item\n2. Second item"
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "ol")
        self.assertEqual(len(result.children[0].children), 2)
        self.assertEqual(result.children[0].children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].children[0].value, "First item")
        self.assertEqual(result.children[0].children[1].tag, "li")
        self.assertEqual(result.children[0].children[1].children[0].value, "Second item")
    
    def test_markdown_to_html_node_multiple_blocks(self):
        markdown = """# Heading

This is a paragraph.

* List item
* Another item"""
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[2].tag, "ul")
    
    def test_markdown_to_html_node_empty(self):
        markdown = ""
        result = blocks.markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 0)
    
    def test_markdown_to_html_paragraph(self):
        markdown = "This is a paragraph."
        html_node = blocks.markdown_to_html_node(markdown)
        html_string = html_node.to_html()
        expected = "<div><p>This is a paragraph.</p></div>"
        self.assertEqual(html_string, expected)
    
    def test_markdown_to_html_heading(self):
        markdown = "# Main Heading"
        html_node = blocks.markdown_to_html_node(markdown)
        html_string = html_node.to_html()
        expected = "<div><h1>Main Heading</h1></div>"
        self.assertEqual(html_string, expected)
    
    def test_markdown_to_html_code_block(self):
        markdown = "```\nprint('hello world')\n```"
        html_node = blocks.markdown_to_html_node(markdown)
        html_string = html_node.to_html()
        expected = "<div><pre><code>print('hello world')</code></pre></div>"
        self.assertEqual(html_string, expected)
    
    def test_markdown_to_html_quote(self):
        markdown = "> This is a quote"
        html_node = blocks.markdown_to_html_node(markdown)
        html_string = html_node.to_html()
        expected = "<div><blockquote>This is a quote</blockquote></div>"
        self.assertEqual(html_string, expected)
    
    def test_markdown_to_html_unordered_list(self):
        markdown = "* Item one\n* Item two"
        html_node = blocks.markdown_to_html_node(markdown)
        html_string = html_node.to_html()
        expected = "<div><ul><li>Item one</li><li>Item two</li></ul></div>"
        self.assertEqual(html_string, expected)
    
    def test_markdown_to_html_ordered_list(self):
        markdown = "1. First\n2. Second"
        html_node = blocks.markdown_to_html_node(markdown)
        html_string = html_node.to_html()
        expected = "<div><ol><li>First</li><li>Second</li></ol></div>"
        self.assertEqual(html_string, expected)
    
    def test_markdown_to_html_mixed_content(self):
        markdown = """# Title

This is a paragraph.

* List item"""
        html_node = blocks.markdown_to_html_node(markdown)
        html_string = html_node.to_html()
        expected = "<div><h1>Title</h1><p>This is a paragraph.</p><ul><li>List item</li></ul></div>"
        self.assertEqual(html_string, expected)





if __name__ == "__main__":
    unittest.main()
