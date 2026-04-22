import unittest
from textnode import TextNode, TextType
from markdown_to_text import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode("This is text with a ![cat](https://i.imgur.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
        ], new_nodes)

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ], new_nodes)

    def test_split_image_at_start(self):
        node = TextNode("![cat](https://i.imgur.com/cat.png) then text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
            TextNode(" then text", TextType.TEXT),
        ], new_nodes)

    def test_split_image_at_end(self):
        node = TextNode("text then ![cat](https://i.imgur.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("text then ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
        ], new_nodes)

    def test_split_image_only(self):
        node = TextNode("![cat](https://i.imgur.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
        ], new_nodes)

    def test_split_image_no_images(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("just plain text", TextType.TEXT)], new_nodes)

    def test_split_image_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("already bold", TextType.BOLD)], new_nodes)

    def test_split_image_mixed_list(self):
        nodes = [
            TextNode("text with ![cat](https://i.imgur.com/cat.png) image", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([
            TextNode("text with ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
            TextNode(" image", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ], new_nodes)

    def test_split_image_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self):
        node = TextNode("This is text with a [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
        ], new_nodes)

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ], new_nodes)

    def test_split_link_at_start(self):
        node = TextNode("[link](https://www.boot.dev) then text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" then text", TextType.TEXT),
        ], new_nodes)

    def test_split_link_at_end(self):
        node = TextNode("text then [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("text then ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
        ], new_nodes)

    def test_split_link_only(self):
        node = TextNode("[link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
        ], new_nodes)

    def test_split_link_no_links(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("just plain text", TextType.TEXT)], new_nodes)

    def test_split_link_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("already bold", TextType.BOLD)], new_nodes)

    def test_split_link_mixed_list(self):
        nodes = [
            TextNode("text with [link](https://www.boot.dev) here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual([
            TextNode("text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ], new_nodes)

    def test_split_link_ignores_images(self):
        node = TextNode("text with ![cat](https://i.imgur.com/cat.png) image", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("text with ![cat](https://i.imgur.com/cat.png) image", TextType.TEXT),
        ], new_nodes)

    def test_split_link_empty_list(self):
        self.assertListEqual([], split_nodes_link([]))

if __name__ == "__main__":
    unittest.main()