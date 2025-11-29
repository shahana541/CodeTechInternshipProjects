import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

DATA_FILE = "data.csv"
CHART_FILE = "chart.png"
REPORT_FILE = "report.pdf"


def load_data(filename):
    """Load and validate data from CSV."""
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    df = pd.read_csv(filename)
    if "Name" not in df.columns or "Score" not in df.columns:
        raise ValueError("CSV must contain 'Name' and 'Score' columns.")
    return df


def calc_statistics(df):
    """Return key statistics as dict."""
    return {
        "Average": df["Score"].mean(),
        "Highest": df["Score"].max(),
        "Lowest": df["Score"].min(),
        "Median": df["Score"].median(),
        "StdDev": df["Score"].std(),
        "Count": len(df),
    }


def plot_chart(df):
    """Generate and save a bar chart."""
    plt.figure(figsize=(7, 4))
    plt.bar(df["Name"], df["Score"], color="#3b8eea")
    plt.title("Student Scores", fontsize=14)
    plt.xlabel("Name")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig(CHART_FILE)
    plt.close()


class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 18)
        self.cell(0, 10, "Student Score Analysis", border=False, ln=1, align="C")
        self.ln(4)
        self.set_draw_color(50, 50, 150)
        self.set_line_width(1)
        self.line(10, 24, 200, 24)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def stats_box(self, stats):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 240, 255)
        self.cell(0, 10, "Summary Statistics", ln=1, fill=True)
        self.set_font("Arial", "", 11)
        for key, value in stats.items():
            self.cell(0, 8, f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}", ln=1, fill=True)
        self.ln(2)

    def add_scores_table(self, df):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(70, 10, "Name", 1, 0, "C", True)
        self.cell(40, 10, "Score", 1, 0, "C", True)
        self.ln()
        self.set_font("Arial", "", 11)
        for i, row in df.iterrows():
            fill = i % 2 == 0
            self.cell(70, 8, row["Name"], 1, 0, "C", fill)
            self.cell(40, 8, f"{row['Score']}", 1, 0, "C", fill)
            self.ln()

    def add_chart(self, chart_path):
        self.ln(5)
        self.cell(0, 8, "Scores Distribution", ln=1, align="C")
        self.image(chart_path, x=40, w=120)
        self.ln(3)

def generate_pdf(df, stats, chart_path, out_file):
    pdf = PDFReport()
    pdf.add_page()
    pdf.stats_box(stats)
    pdf.ln(3)
    pdf.add_chart(chart_path)
    pdf.ln(3)
    pdf.add_scores_table(df)
    pdf.output(out_file)
    print(f"PDF report generated: {out_file}")

def main():
    try:
        df = load_data(DATA_FILE)
        stats = calc_statistics(df)
        plot_chart(df)
        generate_pdf(df, stats, CHART_FILE, REPORT_FILE)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
