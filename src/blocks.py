from typing import List, Optional

def markdown_to_blocks(raw_markdown:str) -> List[str]:
    # Remove excess newlines
    while "\n\n\n" in raw_markdown:
        raw_markdown = raw_markdown.replace("\n\n\n","\n\n")

    pieces = raw_markdown.split("\n\n")
    return list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), pieces)))

    
