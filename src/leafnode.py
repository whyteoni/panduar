from htmlnode import HTMLNode
from typing import Optional

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: Optional[dict] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        # if self.value is None:
        #     raise ValueError("LeafNode has no value defined")
        
        if self.tag is None and self.props:
            raise ValueError("LeafNode cannot have props with a tag")
        
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value or ''}</{self.tag}>"
        else:
            return self.value 
