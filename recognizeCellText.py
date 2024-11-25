"""
Using TSR and TCR annotations from json files, we construct masked images for each cell in the table and retrieve their
text using EasyOCR. We save our results in CSVs for table.
"""

import json
import cv2
import numpy as np
import os
import easyocr
import pandas as pd

datapath = "../data/20647788/TabRecSet/"
json_dir_path = datapath + "TSR_TCR_annotation/"
im_dir_path = datapath + "image/english_all-line/"
basepath = "."
text_csv_dir = "text_csvs"

def detect_text_in_all_tables():
    """
    Generates masked images for each table cell based on the polygons provided in the json files. Detects the text in 
    these masked images and generates a csv of the result for each table.
    """
    json_file_names = os.listdir(json_dir_path)

    for count, json_file_name in enumerate(json_file_names):
        data = load_json(json_dir_path + json_file_name)
        if os.path.exists(im_dir_path + data['imagePath']):
            create_text_csv_for_table(data)
        
        # Update progress
        if count % 500 == 0:
            print("Created cell masks for " + str(count) + "\\" + str(len(json_file_names)))

def load_json(jsonpath):
    """
    Loads in data from a json file.
    Inputs: 
    - jsonpath: the filepath for the json file
    """
    with open(jsonpath, 'r') as file:
        data = json.load(file)

    return data

def create_text_csv_for_table(data):
    """
    Creates a polygon mask for each cell in the table and recognizes the text using EasyOCR. Saves the results to a csv
    Inputs:
    - data: the detected cell information for the table image
    """
    df = pd.DataFrame(columns="position,text,detected_text".split(","))
    
    impath = data['imagePath']
    img_name = impath[:impath.rfind('.')]
    img = cv2.imread(im_dir_path + impath)

    # Create a masked image, detects the text, and adds a line to the df for each table cell
    for shape in data['shapes']:
        position, text = get_position_and_text(shape['label'])

        masked_image = create_masked_image(shape, img)
        detected_text = read_text(masked_image)
        
        df.loc[len(df)] = np.array([position, text, detected_text], dtype=object)

    # Save the csv
    df.to_csv(basepath + "/" + text_csv_dir + "/" + img_name + ".csv", encoding='utf-8', index=False)

def get_position_and_text(label):
    """
    Separates the position and text. The text always comes after the 4th occurrence of '-'.
    Inputs:
    - label: the label provided by the dataset of the form "col-row-colspan-rowspan-text"
    Outputs:
    - position: string of the form "col-row-colspan-rowspan"
    - text: the text from the label
    """
    val = -1
    for i in range(0, 4):
        val = label.find('-', val+1)

    position = label[:val]
    text = label[val+1:]
    return position, text

def create_masked_image(shape, img):
    """
    Combines the image and polygon mask into a masked image.
    Inputs:
    - shape: a list containing the points for a polygon surrounding the table cell
    - img: the image to mask
    Outputs:
    - the masked image in RGB format
    """
    points = np.array(shape['points'])
    mask = create_polygon_mask(img, points)

    masked_image_bgr = (mask * img).astype('int')
    masked_image_rgb = cv2.cvtColor(masked_image_bgr.astype('uint8'), cv2.COLOR_BGR2RGB)
    return masked_image_rgb

def create_polygon_mask(img, points):
    """
    Creates a boolean mask from the polygon created by the given points.
    Inputs:
    - img: a BGR image.
    - points: a list of points assumed to be within the images bounds.
    Outputs:
    - mask: a boolean mask of the polygon
    """
    (h,w,c) = img.shape
    mask = np.zeros((h,w,c), dtype=np.int32)
    
    mask = cv2.fillPoly(mask, pts=np.int32([points]), color=(255, 255, 255))

    mask = mask / 255
    return mask

def read_text(image):
    """
    Given an OpenCV image, returns the English text detected.
    Inputs: an image
    Outputs: the text detected in the image
    """
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    if result == []:
        return ""
    else:
        return result[0][1]

if __name__=="__main__":
    if not os.path.isdir(basepath + "/" + text_csv_dir):
        os.mkdir(basepath + "/" + text_csv_dir)

    detect_text_in_all_tables()