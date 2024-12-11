
import json
import cv2
import numpy as np
import os
import easyocr
import pandas as pd
import zss
import sys

from makeTable import process_shapes, load_json, extract_all_shapes
from recognizeCellText import read_text, create_polygon_mask, create_text_csv_for_table, create_masked_image
from zssTEDS import dataframe_to_tree, count_nodes, simple_cost, Node
from structureMasks import process_masks, replace_text

item_name = '6kpiuhyg'
base_path = '20647788/TabRecSet/'
img_path = f'{base_path}image/english_all-line/{item_name}.jpg'
json_path = f'{base_path}TSR_TCR_annotation/{item_name}.json'

item_name = '6kpiuhyg'

base_path = '20647788/'
img_path = f'{base_path}image/english_all-line/{item_name}.jpg'
json_annotation_path = f'{base_path}/TabRecSet/TSR_TCR_annotation/{item_name}.json'
json_sample_path = f'{base_path}english/{item_name}.json'
mask_path = f'masked_cells/{item_name}'

table1 = process_shapes(json_annotation_path)
table2 = process_shapes(json_sample_path)

# Print the table and save it as csv
print(table1)
print(table2)

# table1 = pd.read_csv('table1.csv')
# table2 = pd.read_csv('table2.csv')


table1.to_csv(f'tables/{item_name}_annotations.csv')
table2.to_csv(f'tables/{item_name}_sample.csv')


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

sys.exit()

# SEM to split into polygons



img = cv2.imread(img_path)

#def add_sem2points(img):

# take img name
# mask folder with name of img
# access all labels in filename for masks
# read text in given coordinate

# Create a masked image, detects the text, and adds a line to the df for each table cell
all_shapes = extract_all_shapes(json_path)

for shape in all_shapes: # get shapes using SEMv2
    masked_image = create_masked_image(shape, img)
    detected_text = read_text(masked_image)
    


masked_image = create_masked_image(shape, img)

json_path = ''
table = process_shapes(json_path)

create_text_csv_for_table(data)



# Evaluates from the JSON file names
def evaluate(file1,file2):
    t1 = load_json(file1)
    t2 = load_json(file2)
    table1 = process_shapes(t1)
    table2 = process_shapes(t2)

    # Convert tables to tree structures
    tree1 = dataframe_to_tree(table1)
    tree2 = dataframe_to_tree(table2)

    num_nodes_tree1 = count_nodes(tree1)
    num_nodes_tree2 = count_nodes(tree2)

    # Calculate the Tree Edit Distance Similarity
    ted = zss.simple_distance(tree1, tree2, Node.get_children, Node.get_label, simple_cost)
    teds = 1 - (ted /  max(num_nodes_tree1, num_nodes_tree2))
    return teds
