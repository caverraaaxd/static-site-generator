from gencontent import extract_title


import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_trailing_whitespace(self):
        self.assertEqual(extract_title("# Hello   "), "Hello")

    def test_no_header_raises(self):
        with self.assertRaises(Exception):
            extract_title("no header here")
  
    
    
    

if __name__ == "__main__":
    unittest.main()