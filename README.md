# BachelorProject-Seatingarrangement

Simple tools for converting sheet responses into project JSON input and running seating algorithms.

## Desktop UI

Use the small Tkinter app when you want a quick manual flow:

1. Pick an `.xlsx` file exported from Google Sheets.
2. Choose an algorithm.
3. Enter table sizes (for example `8,8,6`).
4. Click **Convert + Run**.

The app converts the sheet in memory (no intermediate JSON files are written),
then runs the selected algorithm and shows the resulting arrangement and total score.

Run it with:

```bash
python desktop_ui.py
```

