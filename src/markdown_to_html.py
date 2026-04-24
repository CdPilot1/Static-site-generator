from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type, BlockType
from markdown_to_text import text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import ParentNode, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block)
                inline_children = [text_node_to_html_node(n) for n in text_nodes]
                children.append(ParentNode("p", inline_children))
            
            case BlockType.HEADING:
                level = len(block.split(" ")[0])
                text = block[level+1:]
                text_nodes = text_to_textnodes(text)
                inline_children = [text_node_to_html_node(n) for n in text_nodes]
                children.append(ParentNode(f"h{level}", inline_children))

            case BlockType.CODE:
                text = block[4: -3].strip()
                code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
                children.append(ParentNode("pre", [code_node]))

            case BlockType.QUOTE:
                lines = block.split("\n")
                text = "\n".join(line.lstrip(">").strip() for line in lines)
                text_nodes = text_to_textnodes(text)
                inline_children = [text_node_to_html_node(n) for n in text_nodes]
                children.append(ParentNode("blockquote", inline_children))
            
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                li_nodes = []
                for item in items:
                    text_nodes = text_to_textnodes(item[2:])
                    inline_children = [text_node_to_html_node(n) for n in text_nodes]
                    li_nodes.append(ParentNode("li", inline_children))
                children.append(ParentNode("ul", li_nodes))

            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                li_nodes = []
                for item in items:
                    text = item.split(". ", 1)[1]
                    text_nodes = text_to_textnodes(text)
                    inline_children = [text_node_to_html_node(n) for n in text_nodes]
                    li_nodes.append(ParentNode("li", inline_children))
                children.append(ParentNode("ol", li_nodes))

            case _:
                raise ValueError(f"Unknown block type: {block_type}")
    
    return ParentNode("div", children)