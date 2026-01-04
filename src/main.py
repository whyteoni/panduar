import os
import shutil
import sys
from htmlpage import generate_page

BASE_DIR = os.path.dirname(__file__)
CONTENT_DIR = os.path.abspath(BASE_DIR + "/../content")
PUBLIC_DIR = os.path.abspath(BASE_DIR + "/../docs")
STATIC_DIR = os.path.abspath(BASE_DIR + "/../static")
TEMPLATE_PATH = os.path.abspath(BASE_DIR + "/../template/template.html")

def copy_static_assets(source:str, dest:str) -> None:
    for file in os.listdir(source):
        full_src_path = os.path.join(source, file)
        full_dest_path = os.path.join(dest, file)
        if os.path.isfile(full_src_path):
            shutil.copy(full_src_path, full_dest_path)
            # print(f"COPY: {full_src_path} -> {full_dest_path}")
        else:
            os.mkdir(full_dest_path)
            # print(f"MAKE: {full_dest_path}")
            copy_static_assets(full_src_path,full_dest_path)

def generate_site(from_path:str, template_path:str, dest_path:str, basepath:str) -> None:
    common_path_len = len(os.path.commonpath([from_path,template_path,dest_path])) + 1
    for file in os.listdir(from_path):
        full_src_path = os.path.join(from_path, file)

        if os.path.isfile(full_src_path) and file[-3:] == ".md":
            full_dest_path = os.path.join(dest_path, file[:-2] + "html")
            generate_page(full_src_path, template_path, full_dest_path, basepath)

        elif os.path.isdir(full_src_path):
            full_dest_path = os.path.join(dest_path, file)
            os.mkdir(full_dest_path)
            generate_site(full_src_path, template_path, full_dest_path, basepath)

        else:
            print(f"unprocessable file: {full_src_path[common_path_len:]}")

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    os.mkdir(PUBLIC_DIR)
    copy_static_assets(STATIC_DIR, PUBLIC_DIR)
    generate_site(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR, basepath)

if __name__ == "__main__":
    main()
