import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


class TestHTMLNode(unittest.TestCase):

    def test_htmlnode(self):
        html_node1 = HTMLNode("a", "test_text", ["children1", "children2"], {"href": "https://www.google.com"})
        self.assertEqual(html_node1.tag,"a")
        self.assertEqual(html_node1.value,"test_text")
        self.assertEqual(html_node1.children,["children1", "children2"])
        self.assertEqual(html_node1.props,{"href": "https://www.google.com"})
        


    
    def test_defvals(self):
        html_node1 = HTMLNode()
        self.assertEqual(html_node1.__repr__(),f"HTMLNode({None}, {None}, {None}, {None})")


    def test_props_tohtml(self):
        html_node1 = HTMLNode("a", "test_text", ["children1", "children2"], {"href": "https://www.google.com"})
        self.assertEqual(html_node1.props_to_html(),' href="https://www.google.com"')


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_parent_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node],{"href": "https://www.google.com"})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://www.google.com"><span>child</span></div>',
        )
    
    def test_to_html_with_children_and_children_props(self):
        child_node = LeafNode("span", "child", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span href="https://www.google.com">child</span></div>',
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic_text(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code_text(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {'href': "https://google.com"})
        
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://pinterest.com/kitty--picture")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://pinterest.com/kitty--picture', 'alt': 'This is an image'})

    
    
    
    

if __name__ == "__main__":
    unittest.main()