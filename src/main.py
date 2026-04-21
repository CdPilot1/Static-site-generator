from textnode import TextNode, InlineText

def main():
    node = TextNode("Some text", InlineText.LINK, "https://en.wikipedia.org/wiki/Red-eared_firetail")
    print(node)

main()
