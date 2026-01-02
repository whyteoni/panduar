import re

from enum import Enum
from typing import Optional, List
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text:str, text_type:str | TextType, url: Optional[str]=None):
        self.text = text
        self.text_type = text_type if isinstance(text_type, TextType) else TextType(text_type) 
        self.url = url

    def __eq__(self, other):
        for attr in ["text","text_type","url"]:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node:TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag = "a",
                value = text_node.text,
                props = { "href": text_node.url }
                )
        case TextType.IMAGE:
            return LeafNode(
                tag = "img",
                value = None,
                props = {
                    "alt": text_node.text,
                    "href": text_node.url
                }
            )
        
def split_nodes_delimiter(old_nodes:List[TextNode], delimiter:str, text_type:TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type:
            continue
        
        pieces = node.text.split(delimiter)
        while len(pieces) > 1:
            first = pieces.pop(0)
            second = pieces.pop(0)
            if first:
                new_nodes.append(TextNode(first,node.text_type))
            if second:
                new_nodes.append(TextNode(second,text_type))
        if pieces[0]:
            new_nodes.append(TextNode(pieces[0],node.text_type))
    return new_nodes
            
def extract_markdown_links(text:str) -> List[tuple[str,str]]:
    return re.findall(r"[^\!]\[(.*?)\]\((.+?)\)",text)

def extract_markdown_images(text:str) -> List[tuple[str,str]]:
    return re.findall(r"\!\[(.*?)\]\((.+?)\)",text)

def split_node_images(old_nodes:List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type in [TextType.LINK, TextType.IMAGE, TextType.CODE]:
            # Do not process existing links or images, or code blocks
            new_nodes.append(node)
            continue

        links = extract_markdown_images(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        working_text = node.text
        text_type = node.text_type
        for alt_text,image_url in links:
            before, after = working_text.split(f"![{alt_text}]({image_url})",1)
            if before != "":
                new_nodes.append(TextNode(before, text_type))
            new_nodes.append(TextNode(alt_text,TextType.IMAGE,image_url))
            working_text = after
        
        if working_text != "":
            new_nodes.append(TextNode(working_text, text_type))

    return new_nodes

def split_node_links(old_nodes:List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type in [TextType.LINK, TextType.IMAGE, TextType.CODE]:
            # Do not process existing links or images, or code blocks
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        working_text = node.text
        text_type = node.text_type
        for link_text,link_url in links:
            before, after = working_text.split(f"[{link_text}]({link_url})",1)
            if before != "":
                new_nodes.append(TextNode(before, text_type))
            new_nodes.append(TextNode(link_text,TextType.LINK,link_url))
            working_text = after
        
        if working_text != "":
            new_nodes.append(TextNode(working_text, text_type))

    return new_nodes

def text_to_textnodes(text:str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_node_images(nodes)
    nodes = split_node_links(nodes)
    return nodes
