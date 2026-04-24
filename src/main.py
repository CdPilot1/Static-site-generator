import os
import shutil
from textnode import TextNode, TextType

def copy_directory(src, dst):
    if os.path.exists(dst):
        print(f"Deleting {dst}")
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            print(f"Entering directory {src_path}")
            copy_directory(src_path, dst_path)



def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static = os.path.join(root, "static")
    dst = os.path.join(root, "public")
    copy_directory(static, dst)

main()
