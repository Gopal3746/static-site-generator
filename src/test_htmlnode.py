import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode("a", "docs", None, {"href": "https://x.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://x.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "HI")
        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode("p", "Hi")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hi")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_values_without_props(self):
        node = LeafNode("p", "Hi")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hi")
        self.assertIsNone(node.props)

    def test_values_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me!")
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_to_html_without_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_values(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("b", [child_node])
        self.assertEqual(parent_node.tag, "b")
        self.assertListEqual(parent_node.children, [child_node])

    def test_to_html_with_children(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("b", [child_node])
        self.assertEqual(parent_node.to_html(), '<b><a href="https://www.google.com">Click me!</a></b>')

    def test_to_html_with_grand_children(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("b", [child_node])
        grand_parent_node = ParentNode("div", [parent_node])
        self.assertEqual(grand_parent_node.to_html(), '<div><b><a href="https://www.google.com">Click me!</a></b></div>')

    def test_to_html_with_siblings(self):
        sibling_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        sibling_node2 = LeafNode(None, "Hii")
        parent_node = ParentNode("b", [sibling_node, sibling_node2])
        self.assertEqual(parent_node.to_html(), '<b><a href="https://www.google.com">Click me!</a>Hii</b>')

if __name__ == "__main__":
    unittest.main()
