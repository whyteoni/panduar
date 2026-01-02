from typing import Optional

class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[list] = None, props: Optional[dict] = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __eq__(self,other):
        for attr in ["tag","value","children","props"]:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def to_html(self) -> str:
        html = f"<{self.tag}{self.props_to_html()}>"
        if self.value:
            html += self.value
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
    
    def props_to_html(self):
        if len(self.props) == 0:
            return ""
        
        str_props = []
        for attr, value in self.props.items():
            str_props.append(f"{attr}=\"{value}\"")
        return " " + " ".join(str_props)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
