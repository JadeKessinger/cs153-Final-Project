import pandas as pd
import os

from makeTable import process_shapes
from zssTEDS import evaluate


item_name = '6kpiuhyg'

base_path = '20647788/'
img_path = f'{base_path}image/english_all-line/{item_name}.jpg'
json_annotation_path = f'{base_path}/TabRecSet/TSR_TCR_annotation/{item_name}.json'
json_sample_path = f'{base_path}english/{item_name}.json'
mask_path = f'masked_cells/{item_name}'


# Test if tables exist and if not create them
table1_path = f'tables/{item_name}_annotations.csv'
table2_path = f'tables/{item_name}_sample.csv'
if os.path.isfile(table1_path) and os.path.isfile(table2_path):
    table1 = pd.read_csv(table1_path)
    table2 = pd.read_csv(table2_path)
else:
    table1 = process_shapes(json_annotation_path)
    table2 = process_shapes(json_sample_path)

    table1.to_csv(table1_path)
    table2.to_csv(table2_path)

evaluation = evaluate(table1,table2)


print(f'Tree Edit Distance: {evaluation[0]}')
print(f'Tree Edit Distance Similarity: {evaluation[1]}')
