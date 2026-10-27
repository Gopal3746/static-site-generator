import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from textnode import TextType, TextNode

class TestInlineMarkdown(unittest.TestCase):
    def test_bold_delimiter(self):
        node = TextNode("This is a **bold**word", TextType.TEXT)
        expected = [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("word", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_italic_delimiter(self):
        node = TextNode("This is a _italic_ word", TextType.TEXT)
        expected = [
                TextNode("This is a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT,)
        ]
        self.assertListEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), expected)

    def test_multiiple_textnodes(self):
        node = TextNode("This is a **bold**word", TextType.TEXT)
        node2 = TextNode("This is a **bold** word2", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("word", TextType.TEXT),
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word2", TextType.TEXT,)
        ]
        self.assertListEqual(split_nodes_delimiter([node, node2], "**", TextType.BOLD), expected)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(extract_markdown_images(text),expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_split_nodes_image_with_single_image(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and "
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_image_with_mutiple_images(self):
        text = "This is text with multiple links ![Gopal's GitHub](https://github.com/Gopal3746/), and ![Gopal's YouTube](https://www.youtube.com/@gopalkamineni8552)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with multiple links ", TextType.TEXT),
            TextNode("Gopal's GitHub", TextType.IMAGE, "https://github.com/Gopal3746/"),
            TextNode(", and ", TextType.TEXT),
            TextNode("Gopal's YouTube", TextType.IMAGE, "https://www.youtube.com/@gopalkamineni8552"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_node_with_only_image(self):
        text = "![Gopal's GitHub](https://github.com/Gopal3746/)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Gopal's GitHub", TextType.IMAGE, "https://github.com/Gopal3746/")
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_node_with_multiple_nodes(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and "
        text2 = "This is text with multiple links ![Gopal's GitHub](https://github.com/Gopal3746/), and ![Gopal's YouTube](https://www.youtube.com/@gopalkamineni8552)"
        node = TextNode(text, TextType.TEXT)
        node2 = TextNode(text2, TextType.TEXT)
        new_nodes = split_nodes_image([node, node2])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("This is text with multiple links ", TextType.TEXT),
            TextNode("Gopal's GitHub", TextType.IMAGE, "https://github.com/Gopal3746/"),
            TextNode(", and ", TextType.TEXT),
            TextNode("Gopal's YouTube", TextType.IMAGE, "https://www.youtube.com/@gopalkamineni8552"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_with_single_link(self):
        text = "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another .)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another .)", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_with_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_node_with_only_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_link_with_multiple_nodes(self):
        text = "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another .)"
        text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, TextType.TEXT)
        node2 = TextNode(text2, TextType.TEXT)
        new_nodes = split_nodes_link([node, node2])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another .)", TextType.TEXT),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)
