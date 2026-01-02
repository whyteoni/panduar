import re

from enum import Enum
from typing import List, Optional
from htmlnode import HTMLNode
from textnode import TextNode, text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown:str) -> List[str]:
    # Remove excess newlines
    while "\n\n\n" in markdown:
        markdown = markdown.replace("\n\n\n","\n\n")

    pieces = markdown.split("\n\n")
    return list(
        filter(
            lambda x: len(x) > 0, 
            map(
                lambda x: x.strip(),
                pieces
                )
            )
        )

def block_to_block_type(block:str) -> BlockType:
    if re.match(r"#{1,6}\s+\S+", block):
        return BlockType.HEADING
    if re.fullmatch(r"```.+```", block, flags=re.DOTALL):
        return BlockType.CODE
    
    lines = block.splitlines()

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(re.match("[-*] ", line) for line in lines):
        return BlockType.UNORDERED_LIST
    if test_for_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def test_for_ordered_list(lines:List[str]) -> bool:
    for idx in range(0,len(lines)):
        if not lines[idx].startswith(f"{idx + 1}. "):
            return False
    return True

def markdown_to_html_node(markdown:str) -> HTMLNode:
    base = HTMLNode("div")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = HTMLNode(None)
        match block_type:
            case BlockType.PARAGRAPH:
                block_node.tag = "p"
                block_node.children = paragraph_block_to_html_nodes(block)
            case BlockType.CODE:
                block_node.tag = "pre"
                code_node = HTMLNode("code")
                code_node.value = block[3:-3].strip()
                block_node.children.append(code_node)
            case BlockType.HEADING:
                block_node = heading_block_to_html_node(block)
            case BlockType.QUOTE:
                block_node.tag = "blockquote"
                block_node.value = ""
                for line in block.splitlines():
                    block_node.value += line[2:].strip()
            case BlockType.ORDERED_LIST:
                block_node.tag = "ol"
                block_node.children = list_block_to_html_nodes(block)
            case BlockType.UNORDERED_LIST:
                block_node.tag = "ul"
                block_node.children = list_block_to_html_nodes(block)
            case _:
                raise ValueError("unknown type: {block_type}")
        base.children.append(block_node)
    return base


def paragraph_block_to_html_nodes(block:str) -> List[HTMLNode]:
    html_nodes = []
    text_nodes = text_to_textnodes(block)
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def heading_block_to_html_node(block:str) -> HTMLNode:
    node = HTMLNode()
    level = 0
    while block.startswith("#"):
        level += 1
        block = block[1:]
    node.tag = f"h{level}"
    node.value = block.strip()
    return node

def list_block_to_html_nodes(block:str) -> List[HTMLNode]:
    nodes = []
    for item in block.splitlines():
        list_item = HTMLNode(
            tag = "li",
            value = item.split(" ", maxsplit=1)[1]
        )
        nodes.append(list_item)
    return nodes
