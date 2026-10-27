from enum import Enum
import re

from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def markdown_to_html_node(markdown: str) -> HTMLNode:
    children_nodes: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = " ".join(block.split("\n"))
                node = ParentNode("p", text_to_children(text))
                children_nodes.append(node)

            case BlockType.HEADING:
                level = 0
                while block[level] == "#":
                    level += 1
                node = ParentNode(f"h{level}", text_to_children(block[level + 1:]))
                children_nodes.append(node)

            case BlockType.CODE:
                text_node = TextNode(block[4: -3], TextType.CODE)
                node = text_node_to_html_node(text_node)
                children_nodes.append(ParentNode("pre", [node]))

            case BlockType.QUOTE:
                lines = [line.lstrip('>').strip() for line in block.split('\n')]
                node = ParentNode("blockquote", text_to_children(" ".join(lines)))
                children_nodes.append(node)

            case BlockType.UNORDERED_LIST:
                items: list[HTMLNode] = [
                        ParentNode("li", text_to_children(line[2:]))
                        for line in block.split("\n")
                ]
                children_nodes.append(ParentNode("ul", items))

            case BlockType.ORDERED_LIST:
                lines = block.split('\n')
                items: list[HTMLNode] = [
                    ParentNode("li", text_to_children(line.removeprefix(f"{i}. ")))
                    for i, line in enumerate(lines, start=1)
                ]
                children_nodes.append(ParentNode("ol", items))
    return ParentNode("div", children_nodes)

def extract_title(markdown: str) -> str:
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no h1 header found")
