import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_provided(self):
        url = "https://127.0.0.1"
        node = TextNode("This is a text node", TextType.LINK,url)
        self.assertEqual(node.url, url)

    def test_url_default(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_texttypes(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node1,node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_convert_bold(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_convert_italic(self):
        text_node = TextNode("Italic text", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),"<i>Italic text</i>")

    def test_convert_code(self):
        code = TextNode("Code block", TextType.CODE)
        html_node = text_node_to_html_node(code)
        self.assertEqual(html_node.to_html(), "<code>Code block</code>")

    def test_convert_link(self):
        link_node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_not_equal_different_text(self):
        node1 = TextNode("Different text", TextType.TEXT)
        node2 = TextNode("Another text", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://site1.com")
        node2 = TextNode("Link text", TextType.LINK, "https://site2.com")
        self.assertNotEqual(node1, node2)

    def test_equal_with_same_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_text_node_repr(self):
        node = TextNode("Test text", TextType.BOLD, "https://example.com")
        expected = "TextNode(Test text, bold, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")

    def test_none_url_conversion(self):
        node = TextNode("Text", TextType.TEXT, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)

    



if __name__ == "__main__":
    unittest.main()
