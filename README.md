# cs153-Final-Project

In this project, we explore the feasibility of chaining together a Table Structure Recognition (TSR) model with an Optical Character Recognition (OCR) model. We generate masked images using table cell's bounding boxes provided by the TSR model and retrieve the cell's text using an OCR model. We utilize TabRecSet as our dataset.

We retrieve the cell text using these masked images in `recognizeCellText.py`. This text is stored in CSVs. Note that generating these CSVs for all 5,316 English all-line tables can take hours to run. We digitize the tables as CSVs in `makeTable.py`.

We do an initial investigation of the edit distance for all cells to see how good our OCR model performs in `calculateEditDistance.py` and `analyzeEditDistance.py`. 

Future Steps:
 - Get the TSR annotations from a TSR model (currently, we are using the annotations from the dataset)
 - Try using another OCR model, such as PyTesseract, and compare results
 - Generate the Tree Edit Distance-based Similarity for all tables for analysis
 - Generate plots for our analysis
