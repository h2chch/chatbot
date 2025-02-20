from mistletoe import Document, ast_renderer
from itertools import groupby
import os
from os.path import dirname, join
import sys

def get_cwd():
    try:
        __file__
    except:
        root = os.getcwd()
    else:
        root = dirname(__file__) 
    return root

def get_absolute_path(cwd, file_path):
    absolute_path = ""
    if (sys.platform.startswith("win")):
        absolute_path = file_path.replace("/", "\\") + "\\"
    else:
        absolute_path = file_path.replace("\\", "/") + "/"
    absolute_path = join(cwd, absolute_path)
    return absolute_path

def get_markdown_files(tutorial_path):
    for root, dirs, files in os.walk(tutorial_path, followlinks=True, topdown=True):
        for file in files:
            if file.endswith(".md") or file.endswith("markdown"):
                path = os.path.join(root, file)
                yield path


def get_markdown_title(markdown_path):
     with open(markdown_path, 'r') as file:
        doc = Document(file)
        ast = ast_renderer.get_ast(doc)
        children = ast["children"]
        for child in children:
            if child["type"] == 'Heading' or child["type"] == 'Paragraph':
                for child2 in child["children"]:
                    if child2["type"] == "RawText":
                        content = child2["content"] 
                        return content

def get_tutorials(tutorial_path):
    tutorials = []
    for key, group in groupby(get_markdown_files(tutorial_path), lambda x: dirname(x)):
        tutorial = {}
        tutorial_files = []
        for tutorial_file in group:
            file = {}
            filename = os.path.basename(tutorial_file)
            if (filename == "0.md" or filename == "0.markdown"):
                tutorial["title"] = get_markdown_title(tutorial_file)
            else:
                file["title"] = get_markdown_title(tutorial_file)
                file["path"] = tutorial_file
                tutorial_files.append(file)

        tutorial["files"] = tutorial_files    
        tutorials.append(tutorial)

    return tutorials

def tutorials():
    result = get_tutorials(get_absolute_path(get_cwd(),"tutorial"))
    return result