import unittest
from block_to_block_type import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    # HEADINGS
    def test_heading_h1(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("# Heading 1"))

    def test_heading_h2(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("## Heading 2"))

    def test_heading_h6(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("###### Heading 6"))

    def test_heading_too_many_hashes(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("####### Not a heading"))

    def test_heading_no_space(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("#NoSpace"))

    # CODE
    def test_code_block(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```\nsome code\n```"))

    def test_code_block_multiline(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```\nline one\nline two\n```"))

    def test_code_block_missing_closing(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("```\nsome code"))

    def test_code_block_missing_opening(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("some code\n```"))

    # QUOTE
    def test_quote_single_line(self):
        self.assertEqual(BlockType.QUOTE, block_to_block_type(">this is a quote"))

    def test_quote_with_space(self):
        self.assertEqual(BlockType.QUOTE, block_to_block_type("> this is a quote"))

    def test_quote_multiline(self):
        self.assertEqual(BlockType.QUOTE, block_to_block_type("> line one\n> line two\n> line three"))

    def test_quote_missing_gt_on_one_line(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("> line one\nline two"))

    # UNORDERED LIST
    def test_unordered_list_single_item(self):
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type("- item one"))

    def test_unordered_list_multiple_items(self):
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type("- item one\n- item two\n- item three"))

    def test_unordered_list_missing_space(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("-item one\n-item two"))

    def test_unordered_list_missing_dash_on_one_line(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("- item one\nitem two"))

    # ORDERED LIST
    def test_ordered_list_single_item(self):
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type("1. item one"))

    def test_ordered_list_multiple_items(self):
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type("1. item one\n2. item two\n3. item three"))

    def test_ordered_list_wrong_start(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("2. item one\n3. item two"))

    def test_ordered_list_out_of_order(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("1. item one\n3. item two"))

    def test_ordered_list_missing_space(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("1.item one\n2.item two"))

    # PARAGRAPH
    def test_paragraph(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("just a plain paragraph"))

    def test_paragraph_multiline(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("line one\nline two\nline three"))

    def test_paragraph_with_inline_markdown(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("this has **bold** and _italic_ text"))


if __name__ == "__main__":
    unittest.main()