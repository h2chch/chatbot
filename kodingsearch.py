from mistletoe import Document, ast_renderer
import os
from os.path import dirname, join
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sys
import textwrap

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

def stem(str):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    str_clean = stemmer.stem(str) 
    return str_clean

def get_markdown_paths(help_path):
    markdown_files = []
    for root, dirs, files in os.walk(help_path, followlinks=True):
        for file in files:
            if file.endswith(".md") or file.endswith("markdown"):
                path = os.path.join(root, file)
                markdown_files.append(path)
    
    return markdown_files

def get_markdown_regex(keyword):
    regex_pattern = r"\b({})\b".format(keyword.replace(" ", "|")) 
    regex = re.compile(regex_pattern, re.IGNORECASE)
    return regex

def parse_markdown(markdown_path, regex):
    result = {}
    result["help"] = markdown_path
    result["heading"] = ""
    result["excerpts"] = []

    with open(markdown_path, 'r') as file:
        doc = Document(file)
        ast = ast_renderer.get_ast(doc)
        children = ast["children"]

        for child in children:
            if child["type"] == 'Heading' or child["type"] == 'Paragraph':
                for child2 in child["children"]:
                    if child2["type"] == "RawText":
                        content = child2["content"] 
                        if (content):
                            if not result["heading"]:
                               result["heading"] = content
                            match = regex.findall(content)
                            if match:
                                result["excerpts"].append(textwrap.shorten(content, width=100, placeholder="..."))    
    return result

def parse_markdowns(markdown_paths, regex):
    for markdown_path in markdown_paths:
        yield parse_markdown(markdown_path, regex)    
        
def search(keyword):
    keyword = stem(keyword)
    regex = get_markdown_regex(keyword)
    markdown_paths = get_markdown_paths(get_absolute_path(get_cwd(),"help"))
    search_result = [result for result in parse_markdowns(markdown_paths, regex) if result["excerpts"]]
    return search_result


def replace_markdown(markdown_path, new_path):
    with open(markdown_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = r'(!\[.*?\]\()(.*?)(\))'

    def replace_path(match):
        return f"{match.group(1)}{new_path}{match.group(2).split('/')[-1]}{match.group(3)}"

    new_content = re.sub(pattern, replace_path, content)
    return new_content

def markdown(markdown_path):
    help_path = get_absolute_path(get_cwd(),"help")
    new_markdown = replace_markdown(markdown_path, help_path)
    return new_markdown