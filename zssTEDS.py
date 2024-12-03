import pandas as pd
import zss
from Levenshtein import distance
from makeTable import process_shapes

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
# TEDS = 0.9614617504178482

# Demo with example files (Very bad)
item_name = '6kpiuhyg'
base_path = '20647788/TabRecSet/'
img_path = f'{base_path}image/english_all-line/{item_name}.jpg'
json_path = f'{base_path}TSR_TCR_annotation/{item_name}.json'
bad_json_path = f'{item_name}.json'
# Load tables from JSON files
# table1 = process_shapes(json_path)
# table2 = process_shapes(bad_json_path)    # TEDS = 0.17150503463834565
table2 = process_shapes(bad_json_path)      # TEDS = 0.1671576121964703
table2 = process_shapes(json_path)          # TEDS = 0.846808357130618
# The difference between the csv variation and json version are not identical as expected
# For some reason converting to csv makes it more accurate in this case
# It is unknown if csv is better for all cases
# It is unknown what changes occur converted from json to csv


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
