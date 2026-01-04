import os
from blocks import markdown_to_html_node

TEMPLATES = {"path": "content"}

def extract_title(markdown:str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.split(" ", maxsplit=1)[1].strip()
    raise Exception("no title found")

def generate_page(from_path:str, template_path:str, dest_path:str, basepath:str) -> None:
    common_path_len = len(os.path.commonpath([from_path,template_path,dest_path])) + 1
    print(f"Generating page from {from_path[common_path_len:]} to {dest_path[common_path_len:]} using {template_path[common_path_len:]}")
    with open(from_path) as f:
        markdown = f.read()

    if template_path not in TEMPLATES:
        with open(template_path) as f:
            TEMPLATES[template_path] = f.read()
    
    template = TEMPLATES[template_path]
    
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}",title).replace("{{ Content }}", html)
    if basepath != "/":
        page = page.replace("href=\"/", f"href=\"/{basepath}/")
        page = page.replace("src=\"/", f"src=\"/{basepath}/")

    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_path):
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)
