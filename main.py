"""
Greg Robson & Thomas Yang
CS 303: Data Structures
7/20/2020
Project 2B: Morse Code Encoder / Decoder
"""

from operator import attrgetter


class Node:

    def __init__(self, letter, code):
        self.left = None
        self.right = None
        self.letter = letter
        self.code = code
        self.length = len(code)

    def traverse(self, root):
        res = []
        if root:
            res = self.traverse(root.left)
            res.append(root)
            res = res + self.traverse(root.right)
        return res


def read_morse_file():
    f = open("morse.txt", "r")
    node_list = []
    for line in f:
        letter = None
        code = ""
        for i in line:
            if letter is None:
                letter = i
            else:
                code += str(i)

        code = code.rstrip("\n")
        node_list.append(Node(letter, code))
    f.close()

    node_list = sorted(node_list, key=attrgetter('length'))

    return node_list


def create_tree(node_list, r):
    for i in node_list:  # For every node in the node list
        root = r
        for x in range(0, len(i.code)):  # For every character in that node's code
            if x == (len(i.code) - 1):
                if i.code[x] == "_":
                    print(root.letter + " has " + i.letter + " on the right")
                    root.right = i
                else:
                    print(root.letter + " has " + i.letter + " on the left")
                    root.left = i
            else:
                if i.code[x] == "_":
                    root = root.right
                else:
                    root = root.left


def main():
    nodes = read_morse_file()
    root = Node("root", "")
    for i in nodes:
        print(i.letter + " " + i.code)
    create_tree(nodes, root)

    printout = root.traverse(root)
    for i in printout:
        print(i.letter + " " + i.code)

main()
