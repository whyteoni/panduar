import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_eq(self):
        node1 = LeafNode("p","this is a test")
        node2 = LeafNode("p","this is a test")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = LeafNode("p","this is a test")
        node2 = LeafNode("b","this is a test")
        self.assertNotEqual(node1,node2)

    def test_value_required(self):
        with self.assertRaises(TypeError):
            node = LeafNode(None)  # type: ignore

    def test_bare_text(self):
        text = "this is some text"
        node = LeafNode(None,text)
        self.assertEqual(node.to_html(), text)

if __name__ == "__main__":
    unittest.main()
