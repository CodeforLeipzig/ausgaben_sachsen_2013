#!/usr/bin/python

import codecs

class Node(object):
    """docstring for Node"""
    def __init__(self, name, value, children):
        super(Node, self).__init__()
        self.name = name
        self.value = value
        if self.value == "-":
            self.value = "0"
        self.children = children

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

def line2node(line):
    components = line.split(";")
    return Node(unicode(components[1].strip()), unicode(components[2]), [])


def main():
    lines = []
    with codecs.open("sachsen_finanzen/71137-102Z-clean.csv", encoding="ISO-8859-1") as f:
        lines = f.readlines()

    lines = lines[1:] # skip header line
    nodes = [line2node(l.strip()) for l in lines]
    flare_node = Node("flare", "-", nodes)

    with codecs.open("flare.json", "w", "utf-8") as f:
        f.write(unicode(flare_node.as_json()))


if __name__ == '__main__':
    main()
