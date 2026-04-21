import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="img", props={"src": "https://example.com/image.png"})
        self.assertEqual(node.props_to_html(), ' src="https://example.com/image.png"')

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none_props(self):
        node = HTMLNode(tag="p", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_leading_space(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com"})
        self.assertTrue(node.props_to_html().startswith(" "))


if __name__ == "__main__":
    unittest.main()