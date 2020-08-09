#!/bin/python
import os

def is_dir(path):
    return os.path.isdir(path)

def is_file(path):
    return os.path.isfile(path)

def is_markdown(path):
    return path.endswith(".md") or path.endswith(".MD")

ignoreNodes = [
    "readme",
    "img", "imgs",
    "asset", "assets",
    "summary", "node_modules",
    ".git", "_book", "book",
]

def ignore(path):
    abs_path = os.path.abspath(path)
    basename = os.path.basename(abs_path)
    if is_dir(path):
        return basename in ignoreNodes

    name = os.path.splitext(basename.lower())[0]
    return name in ignoreNodes

class Node():
    def __init__(self, path):
        self.path = path
        self.is_dir = is_dir(path)
        self.is_markdown = is_markdown(path)

        # sub nodes, for file nodes, empty list
        self.dir_nodes = []
        self.file_nodes = []

        if self.is_dir:
            self._scan(path)

    def _scan(self, path):
        l = os.listdir(path)
        for i in range(0, len(l)):
            p = os.path.join(path, l[i])
            if ignore(p):
                print "ignore:", p
                continue

            if is_markdown(p):
                self.file_nodes.append(Node(p))
                continue

            if is_dir(p):
                self.dir_nodes.append(Node(p))
                continue

    @property
    def name(self):
        abs_path = os.path.abspath(self.path)
        basename = os.path.basename(abs_path)
        if self.is_dir:
            return basename
        return os.path.splitext(basename)[0]

    def to_summary(self, indent):
        summary_list = []

        indent_str = " " * 2 * indent
        if self.is_markdown:
            return ["{0}* [{1}]({2})".format(indent_str, self.name, self.path)]

        if self.is_dir:
            dir_item = "{0}* [{1}]({2})".format(
                indent_str, self.name, os.path.join(self.path, "README.md"))

            summary_list.append(dir_item)

            for md_node in self.file_nodes:
                for item in md_node.to_summary(indent + 1):
                    summary_list.append(item)

            for node in self.dir_nodes:
                for item in node.to_summary(indent + 1):
                    summary_list.append(item)

        return summary_list

root = Node(".")

summary = "\n".join(root.to_summary(0))
with open("SUMMARY.md", "w+") as f:
    f.write(summary)

