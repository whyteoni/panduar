from enum import Enum
from typing import Optional
from leafnode import LeafNode

class Bender(Enum):
    AIR_BENDER = "air"
    WATER_BENDER = "water"
    EARTH_BENDER = "earth"
    FIRE_BENDER = "fire"

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

def text_node_to_html_node(text_node:TextNode):
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
        
