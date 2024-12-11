import pandas as pd
import zss
from Levenshtein import distance
from makeTable import process_shapes, load_json

# Define a tree node class
class Node:
    def __init__(self, label):
        self.label = label
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_label(self):
        return self.label

def dataframe_to_tree(df):
    """
    Converts a dataframe table to a tree structure
    Inputs: df  - The desired table's dataframe
    Outputs:    - The tree contructed from the table
    """
    root = Node('root')
    for i, row in df.iterrows():
        row_node = Node(f'row_{i}')
        root.add_child(row_node)
        for j, cell in enumerate(row):
            cell_node = Node(f'cell_{i}_{j}:{cell}')
            row_node.add_child(cell_node)
    return root

def simple_cost(label1, label2):
    if label1 is None or label2 is None:
        return 1
    return distance(label1, label2) / max(len(label1), len(label2))


def count_nodes(node):
    return 1 + sum(count_nodes(child) for child in node.get_children())


def evaluate(table1,table2):
    """
    Compared and evaluates two tables
    Inputs: table1 & table2 - The two tables to be compared
    Outputs:                - The TED and TEDS scored
    """
    tree1 = dataframe_to_tree(table1)
    tree2 = dataframe_to_tree(table2)

    num_nodes_tree1 = count_nodes(tree1)
    num_nodes_tree2 = count_nodes(tree2)

    # Calculate the Tree Edit Distance Similarity
    ted = zss.simple_distance(tree1, tree2, Node.get_children, Node.get_label, simple_cost)
    teds = 1 - (ted /  max(num_nodes_tree1, num_nodes_tree2))
    
    return [ted,teds]

