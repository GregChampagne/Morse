"""
Greg Robson & Thomas Yang
CS 303: Data Structures
7/21/2020
Project 2B: Morse Code Encoder / Decoder
"""

from operator import attrgetter


# Class that governs the nodes of the tree
class Node:

    # Function for initialization of nodes
    def __init__(self, letter, code):
        self.left = None  # Left node
        self.right = None  # Right node
        self.letter = letter  # The letter of the node
        self.code = code  # The morse code of the node
        self.length = len(code)  # Length of the morse code (used for sorting)

    # Recursive function for traversing through the tree (inorder)
    def traverse(self, root):
        nodes = []
        if root:
            nodes = self.traverse(root.left)  # Traverse the left subtree
            nodes.append(root)  # Add the root
            nodes = nodes + self.traverse(root.right)  # Traverse the right subtree
        return nodes


# Function for reading the morse.txt file and creating nodes from it
def read_morse_file():
    f = open("morse.txt", "r")  # Open the morse code file
    node_list = []
    for line in f:  # For every line in the file
        letter = None
        code = ""
        for i in line:  # For every character in the line
            if letter is None:
                letter = i  # Put the letter in the node's letter
            else:
                code += str(i)  # Put the morse code in the node's code

        code = code.rstrip("\n")  # Removes the newline character from the code
        node_list.append(Node(letter, code))  # Create a node with the letter / code
    f.close()  # Close the file

    node_list = sorted(node_list, key=attrgetter('length'))  # Sort the list of nodes by length

    return node_list  # Return the sorted list of nodes


# Function for creating a binary tree based on morse code dots and dashes
def create_tree(node_list, r):
    for i in node_list:  # For every node in the node list
        root = r  # Set / reset the root to the main root
        for x in range(0, len(i.code)):  # For every character in that node's code
            if x == (len(i.code) - 1):  # If at the last dot or dash
                if i.code[x] == "_":
                    root.right = i  # Add the new node right of this one
                else:
                    root.left = i  # Add the new node left of this one

            else:  # If not at the last dot or dash
                if i.code[x] == "_":
                    root = root.right  # Go down right
                else:
                    root = root.left  # Go down left


# Function for decoding morse code into a string of letters
def decode(morse_string, r):
    char_string = ""  # String that will become the decoded message
    root = r
    for i in range(0, len(morse_string)):  # For every character in the morse code
        if morse_string[i] == " ":  # If the character is a space
            if root.letter != "root":
                char_string += root.letter  # Add the current node's letter to the char_string
            elif i > 0:  # Else if it is a space and not the first character
                if morse_string[i - 1] == " ":  # If the character before is also a space
                    char_string += " "  # Add a space to the string
            root = r  # Reset the root

        else:  # If the character is not a space
            if morse_string[i] == "_":  # If it is a dash
                if root.right is not None:
                    root = root.right  # Current node becomes the right node
                    if i == (len(morse_string) - 1):  # If last character
                        char_string += root.letter  # Add that node's letter
                else:  # If the right of the current node is empty
                    return "Incorrect string"  # Send error message
            elif morse_string[i] == ".":  # If it is a dot
                if root.left is not None:  # And the left of the current node isn't empty
                    root = root.left  # Current node becomes the left node
                    if i == (len(morse_string) - 1):  # If last character
                        char_string += root.letter  # Add that node's letter
                else:
                    return "Incorrect string"  # Send error message
            else:  # And the character is not a dash or dot
                return "Incorrect string"  # Send error message

    return char_string  # Returns a decoded message


# Function for encoding a string of letters into morse code
def encode(char_string, r):
    morse_string = ""
    nodes = r.traverse(r)  # Get list of nodes

    for i in char_string:  # For every character in the message
        if i == " ":  # If space, add a space
            morse_string += " "
        else:  # If not a space
            found = False
            x = 0
            while not found:  # Iterate through the node list
                if x == len(nodes):  # If at end, return error message
                    return "Incorrect string"
                if nodes[x].letter == i:  # If letter is found
                    morse_string += nodes[x].code + " "  # Add the morse code to the morse_string
                    found = True
                x += 1

    return morse_string  # Returns an encoded message


# Main function
def main():
    nodes = read_morse_file()  # Read morse.txt and create all nodes
    root = Node("root", "")  # Create the root
    create_tree(nodes, root)  # Create the rest of the tree

    print(decode("__. ._. . __.  ._ _. _..  _ .... ___ __ ._ ...", root))  # Decode example
    print(encode("morse code is cool", root))  # Encode example


main()
