import re
from enum import Enum
from htmlnode import ParentNode, HTMLNode, LeafNode
from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    blocks = []

    spl = markdown.split("\n\n")
    for block in spl:
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks


def block_to_block_type(block) -> BlockType:
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.U_LIST
    
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.O_LIST

    return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    #1
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    #2
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.QUOTE:
             block_nodes.append(quote_to_html_node(block))
        elif block_type == BlockType.U_LIST:
             block_nodes.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.O_LIST:
             block_nodes.append(ordered_list_to_html_node(block))
        elif block_type == BlockType.CODE:
             block_nodes.append(code_to_html_node(block))
        elif block_type == BlockType.HEADING:   
             block_nodes.append(heading_to_html_node(block))
        elif block_type == BlockType.PARAGRAPH:
             block_nodes.append(paragraph_to_html_node(block))
        
    return ParentNode("div", block_nodes)





def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned = line.strip(">").strip()
        cleaned_lines.append(cleaned)
    content = " ".join(cleaned_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
    
def unordered_list_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned = line[2:]
        cleaned_lines.append(cleaned)

    children = []

    for line in cleaned_lines:
        children.append(ParentNode("li", text_to_children(line)))
    

    return ParentNode("ul", children)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned = line.split(". ", 1)[1]
        cleaned_lines.append(cleaned)

    children = []
    for line in cleaned_lines:
        children.append(ParentNode("li", text_to_children(line)))

    return ParentNode("ol", children)


def code_to_html_node(block):

    children = []
    inner = block[3:-3]
    inner = inner.lstrip("\n")
 
    child_node = text_node_to_html_node(TextNode(inner, TextType.TEXT))
    child_code_node = ParentNode("code", [child_node])
    children.append(child_code_node)

    return ParentNode("pre", children)

        

def heading_to_html_node(block):
    level = 0

    for char in block:
        if char == "#":
            level += 1
        else:
            break

    text = block[level + 1:]

    return ParentNode(f"h{level}", text_to_children(text))



def paragraph_to_html_node(block):
    flattened = block.replace("\n", " ")
    return ParentNode("p", text_to_children(flattened))



def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)

    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children