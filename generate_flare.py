#!/usr/bin/python

import codecs


INPUT_FILE = "sachsen_finanzen/71137-102Z-clean.csv"
INPUT_ENCODING = "ISO-8859-1"
OUTPUT_FILE = "flare.json"
OUTPUT_ENCODING = "utf-8"
CSV_DELIMITER = ";"

INDENT_TOLERANCE = 1
INDENT_MIN = 2
INDENT = 3

class Node(object):
    """docstring for Node"""
    def __init__(self, name, value, children):
        super(Node, self).__init__()
        self.name = name
        self.value = value.strip()
        if self.value == "-":
            self.value = "0"
        self.children = children

    def append_child(self, child):
        self.children.append(child)

    def as_json(self):
        s = u'{"name":"' + self.name + '"'
        if len(self.children) > 0:
            s += u', "children":['
            children_strings = [c.as_json() for c in self.children]
            s += u",".join(children_strings)
            s += u']}'
        else:
            s += u', "size":' +  self.value + u'}'
        return s


def lines2nodes(lines):
    #return [line2node(l.strip()) for l in lines]
    stack = []
    last_indent = None
    last_node = None
    for i in range(len(lines)):
        l = lines[i]
        components = l.split(CSV_DELIMITER)
        indent = len(components[0]) + 1 + len(components[1]) - len(components[1].lstrip(' '))
        node = line2node(l)
        if last_indent is not None and indent > last_indent:
            stack.append(last_node)
            last_node.append_child(node)
        elif last_indent is not None and  last_indent - indent <= INDENT_TOLERANCE:
            parent = stack.pop()
            parent.append_child(node)
            stack.append(parent)
        elif last_indent is not None and indent < last_indent:
            indent_diff = last_indent - indent
            while indent_diff >= INDENT_MIN:
                stack.pop()
                indent_diff -= INDENT
            parent = stack.pop()
            parent.append_child(node)
            stack.append(parent)

#        print "indent: " + str(indent) + " stack size: " + str(len(stack))
        last_indent = indent
        last_node = node

    while len(stack) > 1:
        stack.pop()
    nodes = [ stack[0] ]
    return nodes

def line2node(line):
    components = line.split(";")
    node = Node(unicode(components[1].strip()), unicode(components[2]), [])
    return node


def main():
    lines = []
    with codecs.open(INPUT_FILE, encoding=INPUT_ENCODING) as f:
        lines = f.readlines()

    lines = lines[1:] # skip header line
    nodes = lines2nodes(lines)
    flare_node = Node("flare", "-", nodes)

    with codecs.open(OUTPUT_FILE, "w", OUTPUT_ENCODING) as f:
        f.write(unicode(flare_node.as_json()))


if __name__ == '__main__':
    main()
