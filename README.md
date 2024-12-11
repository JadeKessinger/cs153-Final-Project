# cs153-Final-Project

In this project, we explore the feasibility of chaining together a Table Structure Recognition (TSR) model with an Optical Character Recognition (OCR) model. We generate masked images using table cell's bounding boxes provided by the TSR model and retrieve the cell's text using an OCR model. We utilize TabRecSet as our dataset.

We retrieve the cell text using these masked images in `recognizeCellText.py`. This text is stored in CSVs. Note that generating these CSVs for all 5,316 English all-line tables can take hours to run. 

We do an initial investigation of the edit distance for all cells to see how good our OCR model performs. 

To-Dos:
 - Implement Tree Edit Distance Similarity metric
 - Get the TSR annotations from a TSR model (currently, we are using the annotations from the dataset)
 - Generate plots for our analysis

``` 
CS153-FINAL-PROJECT
├── 20647788
│   ├── README.md
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
├── README.md
├── getTextFromJsons.py
├── makeTable.py
├── masked_cells
│   ├── 6kpiuhyg
│   │   └── (png masks)
│   └── ...
├── testerract.py
└── zssTEDS.py


