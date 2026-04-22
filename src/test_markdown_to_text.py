import unittest
from textnode import TextNode, TextType
from markdown_to_text import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestSplitNodesDelimiter(unittest.TestCase):

    # CODE
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    # BOLD
    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    # ITALIC
    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    # multiple delimiters in one node
    def test_split_multiple_occurrences(self):
        node = TextNode("this `one` and `two` are code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("this ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" are code", TextType.TEXT),
        ])

    # non-TEXT nodes are passed through unchanged
    def test_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    # mixed list of text and non-text nodes
    def test_mixed_list(self):
        nodes = [
            TextNode("plain `code` text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("plain ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ])

    # delimiter at the start of the string
    def test_delimiter_at_start(self):
        node = TextNode("`code` then text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE),
            TextNode(" then text", TextType.TEXT),
        ])

    # delimiter at the end of the string
    def test_delimiter_at_end(self):
        node = TextNode("text then `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("text then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

    # no delimiter in the text at all
    def test_no_delimiter(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("just plain text", TextType.TEXT)])

    # missing closing delimiter raises
    def test_missing_closing_delimiter_raises(self):
        node = TextNode("this `code has no closing", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    # empty input list
    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ], matches)

    def test_extract_images_no_images(self):
        matches = extract_markdown_images("This is just plain text with no images")
        self.assertListEqual([], matches)

    def test_extract_images_ignores_links(self):
        matches = extract_markdown_images(
            "This is a [link](https://www.google.com) not an image"
        )
        self.assertListEqual([], matches)

    def test_extract_images_empty_alt_text(self):
        matches = extract_markdown_images("![](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com) and [another](https://www.boot.dev)"
        )
        self.assertListEqual([
            ("link", "https://www.google.com"),
            ("another", "https://www.boot.dev"),
        ], matches)

    def test_extract_links_no_links(self):
        matches = extract_markdown_links("This is just plain text with no links")
        self.assertListEqual([], matches)

    def test_extract_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is an ![image](https://i.imgur.com/zjjcJKZ.png) not a link"
        )
        self.assertListEqual([], matches)

    def test_extract_links_empty_anchor_text(self):
        matches = extract_markdown_links("[](https://www.google.com)")
        self.assertListEqual([("", "https://www.google.com")], matches)

    def test_extract_links_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

if __name__ == "__main__":
    unittest.main()