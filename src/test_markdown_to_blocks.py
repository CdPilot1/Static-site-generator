import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        markdown = "# This is a heading"
        self.assertListEqual(["# This is a heading"], markdown_to_blocks(markdown))

    def test_multiple_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph\n\n- list item one\n- list item two"
        self.assertListEqual([
            "# This is a heading",
            "This is a paragraph",
            "- list item one\n- list item two",
        ], markdown_to_blocks(markdown))

    def test_strips_whitespace(self):
        markdown = "  # This is a heading  \n\n  This is a paragraph  "
        self.assertListEqual([
            "# This is a heading",
            "This is a paragraph",
        ], markdown_to_blocks(markdown))

    def test_multiple_blank_lines_between_blocks(self):
        markdown = "# This is a heading\n\n\n\nThis is a paragraph"
        self.assertListEqual([
            "# This is a heading",
            "This is a paragraph",
        ], markdown_to_blocks(markdown))

    def test_empty_string(self):
        self.assertListEqual([], markdown_to_blocks(""))

    def test_only_whitespace(self):
        self.assertListEqual([], markdown_to_blocks("   \n\n   \n\n   "))

    def test_preserves_single_newlines_within_block(self):
        markdown = "- item one\n- item two\n- item three"
        self.assertListEqual([
            "- item one\n- item two\n- item three",
        ], markdown_to_blocks(markdown))

    def test_full_document(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertListEqual([
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ], markdown_to_blocks(markdown))


if __name__ == "__main__":
    unittest.main()