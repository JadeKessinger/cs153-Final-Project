import json
import cv2
import numpy as np
import easyocr

# From A1
# This is a provided helper function to save images currently in RGB format to disk in RGB format using OpenCV.
def savergb(img, path):
    """
    Saves an RGB image to a specified location.
    Input:
    - img: an RGB image to be saved to disk.
    - path: a string specifying the target save location.
    """
    cv2.imwrite(path, cv2.cvtColor(img.astype('uint8'), cv2.COLOR_RGB2BGR))

def create_polygon_mask(img, points):
    """
    Creates a boolean mask from the polygon created by the given points.
    Input:
    - img: a BGR image.
    - points: a list of points assumed to be within the images bounds.
    """
    (h,w,c) = img.shape
    mask = np.zeros((h,w,c), dtype=np.int32)
    
    mask = cv2.fillPoly(mask, pts=np.int32([points]), color=(255, 255, 255))

    mask = mask / 255
    return mask

datapath = "../data/20647788/TabRecSet/"

with open(datapath + 'TSR_TCR_annotation/_1z6t7pa.json', 'r') as file:
    data = json.load(file)

impath = datapath + 'image/english_all-line/' + data['imagePath']
img = cv2.imread(impath)

points = np.array(data['shapes'][4]['points'])
mask = create_polygon_mask(img, points)

masked_image = (mask * img).astype('int')
masked_image = cv2.cvtColor(masked_image.astype('uint8'), cv2.COLOR_BGR2RGB)

cv2.imwrite('mask.png', masked_image)
