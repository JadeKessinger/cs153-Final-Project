import json
import cv2
import numpy as np
import os

datapath = "../data/20647788/TabRecSet/"
json_dir_path = datapath + "TSR_TCR_annotation/"
im_dir_path = datapath + "image/english_all-line/"

def create_all_masked_images(output_path):
    """
    Creates a folder of masked images for every json file.
    """
    json_file_names = os.listdir(json_dir_path)

    for count, json_file_name in enumerate(json_file_names):
        data = load_json(json_dir_path + json_file_name)
        if os.path.exists(im_dir_path + data['imagePath']):
            create_masked_images_for_json(data, output_path)
        
        # Update progress
        if count % 500 == 0:
            print("Created cell masks for " + str(count) + "\\" + str(len(json_file_names)))

def create_masked_images_for_json(data, output_path):
    """
    Creates a masked image for each table cell in one image.
    Inputs:
    - impath: the path to the image
    - data: the detected cell information for the table image
    """
    # Create a folder for the masked images
    impath = data['imagePath']
    img_name = impath[:impath.rfind('.')]
    if not os.path.exists(output_path + "/" + img_name):
        os.makedirs(output_path + "/" + img_name)

    img = cv2.imread(im_dir_path + impath)

    # Create a masked image for each table cell
    for shape in data['shapes']:
        points = np.array(shape['points'])
        mask = create_polygon_mask(img, points)

        masked_image = (mask * img).astype('int')
        masked_image = cv2.cvtColor(masked_image.astype('uint8'), cv2.COLOR_BGR2RGB)

        label_without_text = shape['label'][:shape['label'].rfind('-')]

        cv2.imwrite(output_path + "/" + img_name + "/" + label_without_text + '.png', masked_image)

def load_json(jsonpath):
    """
    Loads in data from a json file.
    Inputs: the filepath for the json file
    """
    with open(jsonpath, 'r') as file:
        data = json.load(file)

    return data

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

output_path = "masked_cells"
if not os.path.exists(output_path):
    os.makedirs(output_path)

create_all_masked_images(output_path)

# TODO: Read text from masked cells using an OCR model
# import easyocr
# reader = easyocr.Reader(['en'])

# result = reader.readtext('mask.png')

# for detection in result:
#     print(detection[1])