import pandas as pd
import os
from PIL import Image 
import pytesseract
import easyocr
from PIL import Image
import numpy as np
import re

reader = easyocr.Reader(['en']) 
pattern = r'(\d+)-(\d+)-(\d+)-(\d+)'

masked_path = "./masked_cells"

folders = [f for f in os.listdir(masked_path) if os.path.isdir(os.path.join(masked_path, f))]

# Choose a specific folder for now
first_folder_path = f'{masked_path}/{folders[8]}'
print(first_folder_path)

images = [img for img in os.listdir(first_folder_path) if img.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))] 

# Use EasyOCR to read text from the image
for i in range(len(images)):
    img_path = f'{first_folder_path}/{images[i]}'
 
    matches = re.findall(pattern, images[i])
    if matches:
        numbers = list(map(int, matches[0]))
        print(images[i], numbers) 

    img = Image.open(img_path)

    img_np = np.array(img)
    result = reader.readtext(img_np)
    if result: 
        for (bbox, text, prob) in result: print(f"Detected text: {text} (Confidence: {prob:.2f})") 
    else: 
        print("No text detected in the image.")
   

    # print(img)
    # img.show()

    # text = pytesseract.image_to_string(img)
    # print(text)


    



