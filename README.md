# BachelorProject — Seating Arrangement

Tool to convert Google Sheets responses (can come directly from Google Forms) into seating arrangements and run algorithms to generate and optimize seating plans.

This repository contains a desktop GUI that converts a sheet export, runs a selected algorithm (or a custom pipeline), and displays the resulting arrangement and score.

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Notes:
- This project requires Python 3.10+ (uses modern type annotations).
- The GUI requires `tkinter` (usually included with CPython). On some Linux distributions you must install it separately (e.g. `sudo apt install python3-tk`).

## Run the Desktop UI

Start the GUI from PowerShell:

```powershell
python .\desktop_ui.py
```

If you prefer PyPy and have it installed, run:

```powershell
pypy .\desktop_ui.py
```

## How to use the UI

1. Click "Browse" and select an `.xlsx` file exported from Google Sheets. You can download an example file here: https://doc-0s-7k-sheets.googleusercontent.com/export/imsicvtuc4aajstv90qhvda5c8/6dht2ec2v6h0k70ak1k0odo680/1778604785000/107616245000139511774/107616245000139511774/10Ox8PY-YAueR59mdqU3sreXtxe67oqBDheM5MsPc-d4?format=xlsx&id=10Ox8PY-YAueR59mdqU3sreXtxe67oqBDheM5MsPc-d4&dat=APiwnZJfAJyUN3ofJCftJj_gG02XkdNbQJfxv38Wu7Wgq4UxL79ErqH4dluyr5htSywvTp8IPD5U7IUKmMeVrPuUkd8CF5Mun5VR2GGg3hlZfUDzyLT0vP86Iz76JUVZH3OBCPlqQUk3oUP410yRLCl3gqnNSbwfm95JTfYXm5A5nrgxEok8tuq8JUDdAJhmhgKzIYr7tavO7-Otvo9-HMc9uuA_VDZQVhpHR-kWQ-xqbEOhgvL8aMOZZBOlZpzNmdVysT3Xsa7WQrJDgWc7V2XzTIpHC4n56PFefMhVb0QocHNtyMITJoLQxne6V1t_xA9t-16eV_GF_PUQ7SykF9HMx9lr8A5hVCp8PB4hKq32lwwkq8lr0m496GIWfG8oYqGsrc1xc1kmX84RVn-8S3_DTG_SHN01NpdlCSMxu2orfirYgsuXmV3gJQM74quz9mNFcbPe1mVENucaP55bhOu9W2lOqndpfLiSNQXdTzQ33_NYiI_zTWIw0K7Tpzvu4EHKZUZMV4U-p6Nn7HjDX3Ia766ihQpY22-RRli7-KQSdDJhySzJi6fcuMeSo5vC9rBmTffExc451RWNFv9o9CvBoWdFSAyi-y0eOpG9QY530P3A-EUtwTj4oWfCFe2KdqkBUACb9mbWnc2TRJtMgbxqJydgZz-gGRn8y0wsQqvJbJbYJ9Vn9EnXxJH4IsNi1Vm1HxSjiuA_NG7CX2lzLQwGZNgITe5HevYDRGxCGL0uDYsgvFcLM7kc9CFTMnIPpUs5lZzuvP3PDw1jDOM3KwT3GcepbhF39y2r8fnfBy_T6tJeII7hAw5o-mvbYARlR8AQc9tIstF_zga_QI4y0x7qMl7-32L4iUBmSUWLoFVU9jdbOu3K3STrgKztbzirQ3a1B9HGq1MmrI4TOD2oCmNyiOOvpxRzMlhfMmLh3FzjAt5JV4yCbmoZdAjxcuAnAw-GF2n5oaPfH93m5-Oi-CnZOOXusGxHkJ6uTQ
2. Pick an algorithm from the dropdown, or select `buildOwn` to construct a custom pipeline.
3. Enter table sizes. Accepted formats:
   - Single size: `8` — creates all tables with 8 seats
   - List of sizes: `8,8,6` or `8 8 6` or `8;8;6` — creates tables with those exact sizes
4. Click the "Build + Run" button. The app converts the sheet and run the algorithm(s).

Results are shown inside the GUI.


## The `.xlsx` format
The .xlsx file is made to work directly with Google Forms responses, it should have two sheets.

First Sheet:
- Google Forms will call this sheet "Formularsvar 1", the sheet should ALWAYS have this name (also if not created from Google Forms).
- This sheet can just be directly exported from Google Forms, or created manually with the same format.
- The first row is the header, with column names.
- The first column is the time stamp of the response (this can be empty if not created from Google Forms).
- The second column is ID for the respondent, it should be unique for each respondent, this is the column Google Forms puts the first question in, so the first question should be asking for some kind of ID (e.g. name, email, student number).
- The rest of the columns are the questions and answers. The column names (in the header) are the questions.

Second Sheet:
- The file should also have a second sheet called "Define Answers", you can copy the one from the example file, or create your own, but it should have the same format.
- It is used to define how the answers in the first sheet should be interpreted.
- The first row of the "Define Answers" sheet is the header, with column names.
- The first column is for the questions, the example file will automatically extract them from the first sheet, but this column could just be empty.
- The second column is where you write how the questions should be interpreted, either "preference" or "trait" (see below).
- The third and last column is for the weight of the question, this can be any number you want. The weight is used in the scoring function, so the higher the weight, the more important that question is for the score.

Presences:
- A preference question asks about Id´s of other people. For example "Who do you want to sit with?" or "Who do you want to sit away from?".
- The answer to a preference question can be a single or a list of Id´s separated by commas, spaces, or semicolons.
- The weight of a preference question should be negative if you want people to be separated, and positive if you people want people to be together, based on this.
- Example: If the question is "Who do you want to sit with?" and the answer is "Alice, Bob", and the weight is 5, then the score will increase by 5 (scaled by distance) for each of Alice and Bob that are in the same table as the respondent.

Traits:
- A trait question asks about a trait of the respondent. For example "What is your major?".
- The answer to a trait question can be a single or a list of [answers] separated by commas, spaces, or semicolons. 
- The weight of a trait question should be negative if you want people with the same trait to be separated, and positive if you want people with the same trait to be together, based on this.
- Example: If the question is "What is your major?" and the answer is "Computer Science", and the weight is -3, then the score will decrease by -3 (scaled by distance) for each person with the same major that is in the same table as the respondent.

## Troubleshooting

- Missing tkinter: install the system package (Linux) or install a Python distribution that bundles tkinter.
- If an `.xlsx` file is rejected, ensure it's a valid Excel file exported from Google Sheets and that required columns are present.
- If you see type/annotation errors, verify you are running Python 3.10 or newer.





