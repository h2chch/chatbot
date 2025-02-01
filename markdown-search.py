import re
import os
from os.path import dirname, join

file_dir = "md"
md_files = []

for root, dirs, files in os.walk(file_dir, followlinks=True):
    for file in files:
        if file.endswith(".md") or file.endswith("markdown"):
            path = os.path.join(root, file)
            md_files.append(path)

