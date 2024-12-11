# cs153-Final-Project

In this project, we explore the feasibility of chaining together a Table Structure Recognition (TSR) model with an Optical Character Recognition (OCR) model. We generate masked images using table cell's bounding boxes provided by the TSR model and retrieve the cell's text using an OCR model. We utilize TabRecSet as our dataset.

We retrieve the cell text using these masked images in `recognizeCellText.py`. This text is stored in CSVs. Note that generating these CSVs for all 5,316 English all-line tables can take hours to run. We digitize the tables as CSVs in `makeTable.py`.

We do an initial investigation of the edit distance for all cells to see how good our OCR model performs in `calculateEditDistance.py` and `analyzeEditDistance.py`. 


Within the file `demo.py` we have a functioning demo for a test table. The purpose of this demo is to compare the json annotations, and the predicted table json as included within TabRecSet. This means we measure the TEDS score for that example. This is a set of each file for the `6kpiuhyg` table that maintains the structure used in the full TabRecSet database so it can be easily imported and used for any example.

There is also the file `demoMulti.py` which essentially is a copy of `demo.py` but slightly adjusted to the case of a larger sample size(default is 50 tables). This instead of just returning a single sample it prints an array of every file and its score, then finally the average TEDS score.


Our folder structure is as follows:
``` 
CS153-FINAL-PROJECT
├── 20647788
│   ├── TabRecSet
│   │   ├── TSR_TCR_annotation
│   │   │   ├── 6kpiuhyg.json
│   │   │   └── (all table .json annotations)
│   │   └── image
│   │       ├── english_all-line
│   │       │   ├── 6kpiuhyg.jpg
│   │       │   └── (all table .jpg images)
│   │       └── ...
│   └── english
│       ├── 6kpiuhyg.json
│       └── (all table .json results)
├── masked_cells
│   ├── 6kpiuhyg
│   │   └── (png masks)
│   └── ...
├── analyzeEditDistance.py
├── calculateEditDistance.py
├── demo.py
├── demoMulti.py
├── makeTable.py
├── recognizeCellText.py
├── structureMasks.py
└── zssTEDS.py


Future Steps:
 - Get the TSR annotations from a TSR model (currently, we are using the annotations from the dataset)
 - Try using another OCR model, such as PyTesseract, and compare results
 - Generate the Tree Edit Distance-based Similarity for all tables for analysis
 - Generate plots for our analysis