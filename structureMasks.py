
import os
import pandas as pd
import numpy as np

def get_files(folder_path):
    """
    Converts a folder of image masks into a table where each position is the filename for the desired text to be read.
    Inputs:     folder_path - The folder path containing all the mask PNGs.
    Outputs:    cell_coords - Matrix containing desired paths shape label formatted as
                (x,y,w,h,text) for each shape stored as a large array
    """         
    all_cells = []
    cell_coords = []
    for filename in os.listdir(folder_path):
        # Check if it's a file (and not a directory)
        if os.path.isfile(os.path.join(folder_path, filename)):
            all_cells.append(filename)

            file = os.path.splitext(filename)[0]
            file_split = file.split('-',4)

            for i in range(4):
                file_split[i] = int(file_split[i]) - 1 + i // 2 
            
            file_split.append(filename)
            cell_coords.append(file_split)

    return cell_coords


def process_masks(folder_path):
    """
    Converts folder of image masks into a table where each position is the filename for desired text to be read
    Inputs:     folder_path - The folder path containing all the mask pngs
    Outputs:    table       - a dataframe table with all of the filenames in proper positions
    """

    coords = get_files(folder_path)

    # Calculate the dimensions of the table
    maxr = 0
    maxc = 0
    for cell in coords:
        maxr = max(maxr, cell[0]+cell[2])
        maxc = max(maxc, cell[1]+cell[3])

    # Innitialize the table using max coords   
    table = pd.DataFrame(np.nan, index=range(maxr), columns=range(maxc)).astype(str)
    
    # Set each row and column to the proper text in given position 
    for i in range(len(coords)):
        for r in range(coords[i][0],coords[i][0]+coords[i][2]):
            for c in range(coords[i][1],coords[i][1]+coords[i][3]):
                table.iat[r, c] = coords[i][4]

    return table

def read_text(mask_path):
    return f'foundtext_{mask_path}'

def replace_text(folder_path):
    mask_table = process_masks(folder_path)

    text_table = mask_table.applymap(read_text)
    return text_table
