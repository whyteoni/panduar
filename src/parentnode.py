from typing import List, Optional
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:List[HTMLNode], props: Optional[dict]=None):
        super().__init__(
            tag=tag,
            value=None,
            children=children,
            props=props
        )

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag cannot be None")
        
        if self.children is None:
            raise ValueError("children cannot be None")
        
        html = [f"<{self.tag}{self.props_to_html()}>"]
        for child in self.children:
            html.append(child.to_html())
        html.append(f"</{self.tag}>")

        return "".join(html)

