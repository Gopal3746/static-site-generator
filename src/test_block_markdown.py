import textwrap
import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_with_perfect_syntax(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_block_markdown_with_multi_line_spaces(self):
        md = """
This is paragraph 1



This is paragraph 2
        """
        expected = [
            "This is paragraph 1",
            "This is paragraph 2"
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_block_to_block_type_for_heading_1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_for_heading_with_no_space(self):
        block = "#This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_for_heading_with_4_spaces(self):
        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_for_code(self):
        block = """```
This is a code block
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_for_quote(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_for_quote_two_spaces(self):
        block = ">  This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_for_quote_two_arrows(self):
        block = ">>  This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_for_unordered_list(self):
        block = """- This is first item
- This is second item"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_for_unordered_list_with_no_spaces(self):
        block = """-This is first item
- This is second item"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_for_ordered_list(self):
        block = """1. This is first item
2. This is second item"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_for_ordered_list_no_sequential_order(self):
        block = """8. This is first item though
        """
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_for_paragraph_using_random(self):
        block = """
                jj
        !@ Gopal
        """
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
