import unittest

from leafnode import LeafNode
from parentnode import ParentNode

TEST_NODES = {
    "para": {
        "node": LeafNode("p","this is some text"),
        "text": "this is some text",
        "tag": "p",
        "props": None
    },
    "bare": {
        "node": LeafNode(None, "this is some bare text"),
        "text": "this is some bare text",
        "tag": None,
        "props": None
    },
    "props": {
        "node": LeafNode("p","I got props y'all", {"style": "test", "font": "test"}),
        "text": "I got props y'all",
        "tag": "p",
        "props": 'style="test font="test"'
    }
}


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        p1 = ParentNode("div",[TEST_NODES["para"]["node"]])
        p2 = ParentNode("div",[TEST_NODES["para"]["node"]])
        self.assertEqual(p1, p2)

def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

if __name__ == "__main__":
    unittest.main()
