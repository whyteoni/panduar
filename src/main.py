import os
import shutil

SCRIPT_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.abspath(SCRIPT_DIR + "/../static")
PUBLIC_DIR = os.path.abspath(SCRIPT_DIR + "/../public")

def copy_static_assets(source:str, dest:str) -> None:
    for file in os.listdir(source):
        full_src_path = os.path.join(source, file)
        full_dest_path = os.path.join(dest, file)
        if os.path.isfile(full_src_path):
            shutil.copy(full_src_path, full_dest_path)
            print(f"COPY: {full_src_path} -> {full_dest_path}")
        else:
            os.mkdir(full_dest_path)
            print(f"MAKE: {full_dest_path}")
            copy_static_assets(full_src_path,full_dest_path)

def main():
    shutil.rmtree(PUBLIC_DIR)
    copy_static_assets(STATIC_DIR, PUBLIC_DIR)


if __name__ == "__main__":
    main()
