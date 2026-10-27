from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    IMAGE = "image"
    LINK = "link"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: "TextNode") -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            leaf_node = LeafNode(None, text_node.text)
            return leaf_node
        case TextType.BOLD:
            leaf_node = LeafNode("b", text_node.text)
            return leaf_node
        case TextType.ITALIC:
            leaf_node = LeafNode("i", text_node.text)
            return leaf_node
        case TextType.CODE:
            leaf_node = LeafNode("code", text_node.text)
            return leaf_node
        case TextType.LINK:
            leaf_node = LeafNode("a", text_node.text, {"href": text_node.url})
            return leaf_node
        case TextType.IMAGE:
            leaf_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return leaf_node
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
