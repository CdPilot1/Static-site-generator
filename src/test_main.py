import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual("Hello", extract_title("# Hello"))

    def test_title_with_text_below(self):
        self.assertEqual("Hello", extract_title("# Hello\n\nsome paragraph text"))

    def test_no_heading_raises(self):
        with self.assertRaises(ValueError):
            extract_title("just plain text")

    def test_h2_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Not an h1")


if __name__ == "__main__":
    unittest.main()