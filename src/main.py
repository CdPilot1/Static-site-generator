import os
import shutil
from markdown_to_html import markdown_to_html_node
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

def extract_title(markdown):
    if markdown.startswith("# "):
        return markdown[2:].split("\n")[0]
    raise ValueError("Markdown must start with a heading")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    html_content = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    html = template_content.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)



def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static = os.path.join(root, "static")
    dst = os.path.join(root, "public")
    copy_directory(static, dst)
    generate_page(
        os.path.join(root, "content/index.md"),
        os.path.join(root, "template.html"),
        os.path.join(dst, "index.html")
    )

if __name__ == "__main__":
    main()
