import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        node = markdown_to_html_node("this is a paragraph")
        self.assertEqual(node.to_html(), "<div><p>this is a paragraph</p></div>")

    def test_paragraph_with_inline(self):
        node = markdown_to_html_node("this is **bold** and *italic*")
        self.assertEqual(node.to_html(), "<div><p>this is <b>bold</b> and <i>italic</i></p></div>")

    def test_heading_h1(self):
        node = markdown_to_html_node("# Heading 1")
        self.assertEqual(node.to_html(), "<div><h1>Heading 1</h1></div>")

    def test_heading_h3(self):
        node = markdown_to_html_node("### Heading 3")
        self.assertEqual(node.to_html(), "<div><h3>Heading 3</h3></div>")

    def test_code_block(self):
        node = markdown_to_html_node("```\nsome code\n```")
        self.assertEqual(node.to_html(), "<div><pre><code>some code</code></pre></div>")

    def test_quote_block(self):
        node = markdown_to_html_node("> this is a quote")
        self.assertEqual(node.to_html(), "<div><blockquote>this is a quote</blockquote></div>")

    def test_quote_multiline(self):
        node = markdown_to_html_node("> line one\n> line two")
        self.assertEqual(node.to_html(), "<div><blockquote>line one\nline two</blockquote></div>")

    def test_unordered_list(self):
        node = markdown_to_html_node("- item one\n- item two\n- item three")
        self.assertEqual(node.to_html(), "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>")

    def test_ordered_list(self):
        node = markdown_to_html_node("1. item one\n2. item two\n3. item three")
        self.assertEqual(node.to_html(), "<div><ol><li>item one</li><li>item two</li><li>item three</li></ol></div>")

    def test_multiple_blocks(self):
        node = markdown_to_html_node("# Heading\n\nA paragraph\n\n- list item")
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>A paragraph</p><ul><li>list item</li></ul></div>"
        )

    def test_list_with_inline_markdown(self):
        node = markdown_to_html_node("- **bold** item\n- *italic* item")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li></ul></div>"
        )

    def test_returns_div(self):
        node = markdown_to_html_node("some text")
        self.assertEqual(node.tag, "div")


if __name__ == "__main__":
    unittest.main()