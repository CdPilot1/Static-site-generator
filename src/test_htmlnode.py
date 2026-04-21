import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "click here", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">click here</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "photo", {"src": "image.png", "alt": "a photo"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="a photo">photo</img>')

    def test_leaf_repr(self):
        node = LeafNode("p", "hello", {"class": "text"})
        self.assertEqual(repr(node), "LeafNode(p, hello, {'class': 'text'})")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multiple_children(self):
        parent_node = ParentNode("p", [
            LeafNode("b", "bold"),
            LeafNode("i", "italic"),
            LeafNode(None, " plain"),
        ])
        self.assertEqual(parent_node.to_html(), "<p><b>bold</b><i>italic</i> plain</p>")

    def test_to_html_deep_nesting(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode("b", "deep")
                ])
            ])
        ])
        self.assertEqual(node.to_html(), "<div><section><p><b>deep</b></p></section></div>")

    def test_to_html_multiple_parent_children(self):
        node = ParentNode("div", [
            ParentNode("p", [LeafNode("b", "first")]),
            ParentNode("p", [LeafNode("i", "second")]),
        ])
        self.assertEqual(node.to_html(), "<div><p><b>first</b></p><p><i>second</i></p></div>")

    def test_to_html_with_props(self):
        node = ParentNode("a", [LeafNode(None, "click here")], {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">click here</a>')

    def test_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("p", "hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()