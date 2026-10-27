from pydoc import html
import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text Node", TextType.LINK, url="https://www.youtube.com/")
        node1 = TextNode("This is a text Node", TextType.LINK, url="https://www.youtube.com/")
        self.assertEqual(node, node1)

    def test_ne_with_text(self):
        node = TextNode("This is text node 1", TextType.IMAGE)
        node2 = TextNode("This is text node 2", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_ne_with_type(self):
        node = TextNode("This is text node with TextType Image", TextType.IMAGE)
        node2 = TextNode("This is text node with TextType Bold", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        self.assertEqual(html_node.to_html(), "<i>This is an italic text node</i>")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")

    def test_link(self):
        node = TextNode("Click Me!", TextType.LINK, "https://www.youtube.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click Me!")
        self.assertEqual(html_node.to_html(), '<a href="https://www.youtube.com/">Click Me!</a>')

    def test_image(self):
        node = TextNode("Its a car", TextType.IMAGE, "https://picsum.photos/536/354")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="https://picsum.photos/536/354" alt="Its a car"></img>')

    def test_invalid_TextType(self):
        node = TextNode("Its invalid TextType", "TextType.SOAP")
        with self.assertRaises(ValueError):
                text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
