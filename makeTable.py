import json
import pandas as pd
import numpy as np

def load_json(jsonpath):
    """
    Loads in data from a json file.
    Inputs: the filepath for the json file
    """
    with open(jsonpath, 'r') as file:
        data = json.load(file)
    return data

def extract_all_shapes(json_path):
    """
    Converts a json file into its labeled coords and text for all shapes
    Inputs: json_path   - The filepath for the json file
    Outputs: Matrix containing desired paths shape label formatted as
            (x,y,w,h,text) for each shape stored as a large array
    """
    data = load_json(json_path)
    labels = []
    for label in data['shapes']:
        # Split the first 4 hyphens to separate coords
        split_labels = label['label'].split('-',4)

        # Convert all coords to ints then shift them to start at 0,0
        for i in range(4):
            split_labels[i] = int(split_labels[i]) - 1 + i // 2 
        
        labels.append(split_labels)
        
    return labels


def process_shapes(json_path):
    """
    Converts json shapes to a pandas table  
    Inputs: json_path   - The filepath for the json file
    Outputs: table - a table with all of the json shapes read from json_path
    """

    all_shapes = extract_all_shapes(json_path)

    # Calculate the dimensions of the table
    maxr = 0
    maxc = 0
    for cell in all_shapes:
        maxr = max(maxr, cell[0]+cell[2])
        maxc = max(maxc, cell[1]+cell[3])

    # Innitialize the table using max coords   
    table = pd.DataFrame(np.nan, index=range(maxr), columns=range(maxc)).astype(str)
    
    # Set each row and column to the proper text in given position 
    for x, y, w, h, text in all_shapes:
        for r in range(x, x + w):
            for c in range(y, y + h):
                table.iat[r, c] = text
    return table

item_name = '140129519' # Example item name
base_path = '20647788/TabRecSet/'
img_path = f'{base_path}image/english_all-line/{item_name}.jpg'
json_path = f'{base_path}TSR_TCR_annotation/{item_name}.json'

table = process_shapes(json_path)

# Print the table and save it as csv
print(table)
table.to_csv('table.csv')