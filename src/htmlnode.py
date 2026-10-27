class HTMLNode:
    def __init__(self, tag: str | None = None,
                     value: str | None = None,
                     children: list["HTMLNode"] | None = None,
                     props: dict[str, str] | None = None) -> None:
            self.tag = tag
            self.value = value
            self.children = children
            self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        res = ""
        if self.props is not None:
            for key, value in self.props.items():
                res += f' {key}="{value}"'
        return res

    def __repr__(self) -> str:
         return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
         super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        if self.children is None:
            raise ValueError("No Children")
        inner = ""
        for child in self.children:
            inner += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>"
