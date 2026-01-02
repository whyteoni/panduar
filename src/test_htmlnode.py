import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p","this is a test")
        node2 = HTMLNode("p","this is a test")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode("p","this is a test")
        node2 = HTMLNode("b","this is a test")
        self.assertNotEqual(node1,node2)

    def test_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_props2html(self):
        props = (
            {"href": "https://127.0.0.1", "target": "_blank"},
            " href=\"https://127.0.0.1\" target=\"_blank\""
        )
        node = HTMLNode(props=props[0])
        self.assertEqual(node.props_to_html(),props[1])

if __name__ == "__main__":
    unittest.main()
