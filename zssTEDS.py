import pandas as pd
import zss
from Levenshtein import distance

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

# Convert a pandas DataFrame to a tree structure
def dataframe_to_tree(df):
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


# Load tables from CSV files
table1 = pd.read_csv('table1.csv')
table2 = pd.read_csv('table2.csv')

# Convert tables to tree structures
tree1 = dataframe_to_tree(table1)
tree2 = dataframe_to_tree(table2)

num_nodes_tree1 = count_nodes(tree1)
num_nodes_tree2 = count_nodes(tree2)

# Calculate the Tree Edit Distance Similarity
ted = zss.simple_distance(tree1, tree2, Node.get_children, Node.get_label, simple_cost)
teds = 1 - (ted /  max(num_nodes_tree1, num_nodes_tree2))

print(f'Tree Edit Distance: {ted}')
print(f'Tree Edit Distance Similarity: {teds}')
