import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestSplitDelimeter(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_block_type_heading(self):
        block = "#### Hello boys."
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\ncode block```"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> Quote block."
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered(self):
        block = "- Test\n- Undordered list"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.U_LIST)

    def test_block_to_block_type_ordered(self):
        block = "1. Test\n2. Odordered list"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.O_LIST)


    def test_block_to_block_type_paragraph(self):
        block = "Henlo"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)




    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

    def test_quote_simple(self):
        md = """
> This is a simple quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a simple quote</blockquote></div>",
        )


    def test_quote_with_inline(self):
        md = """
> This quote has **bold** and _italic_ text
> and even a `code` snippet
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This quote has <b>bold</b> and <i>italic</i> text and even a <code>code</code> snippet</blockquote></div>",
        )

    def test_heading_h1(self):
        md = """
# Hello World
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Hello World</h1></div>",
        )

    def test_heading_mixed(self):
        md = """
# Main Title

This is a paragraph under the title.

## Subsection

Another paragraph here.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Title</h1><p>This is a paragraph under the title.</p><h2>Subsection</h2><p>Another paragraph here.</p></div>",
        )




    def test_unordered_list(self):
        md = """
- Item one
- Item **two**
- Item _three_
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item one</li><li>Item <b>two</b></li><li>Item <i>three</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First
2. Second with `code`
3. Third
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First</li><li>Second with <code>code</code></li><li>Third</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()