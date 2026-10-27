from textnode import TextNode, TextType

def main():
    test_object = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(repr(test_object))

main()
