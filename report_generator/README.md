
# How to Run the Report Generator Project

Follow these simple steps to set up and run the project on your machine:

## 1. Clone or Download the Project

Make sure you have all project files including:

- `data.csv` (the input data file)
- `report_generator.py` (main script)
- `requirements.txt` (list of dependencies)

***

## 2. Create and Activate a Python Virtual Environment (Recommended)

Open a terminal or PowerShell in the project folder and run:

For Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

For macOS/Linux terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

***

## 3. Install Project Dependencies

With the virtual environment activated, install required Python packages:

```bash
pip install -r requirements.txt
```

This installs libraries such as pandas, fpdf, and matplotlib.

***

## 4. Run the Report Generator Script

Simply run:

```bash
python report_generator.py
```

The script will:

- Read and analyze data from `data.csv`.
- Generate a bar chart image `chart.png`.
- Generate a detailed PDF report as `report.pdf`.

***

## 5. View the Output

Open `report.pdf` to review the generated report and `chart.png` for the bar chart visualization.

***

## 6. (Optional) Generate Larger Data for Testing

You can create larger test datasets by running any custom data generator script (if included) or by manually expanding `data.csv`.

***

## Troubleshooting

- Ensure you are using Python 3.7 or above.
- Activate the virtual environment before installing packages or running the script.
- If package installation fails, update pip with:
  
  ```bash
  python -m pip install --upgrade pip setuptools wheel
  ```

- Make sure your command prompt or terminal’s current directory is the project root where `report_generator.py` exists.

