import pandas as pd
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Student Score Report", ln=True, align='C')
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        page = "Page " + str(self.page_no())
        self.cell(0, 10, page, align='C')

def add_table_header(pdf):
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, "Name", border=1)
    pdf.cell(40, 10, "Score", border=1, align='R')
    pdf.ln()

def add_table_row(pdf, name, score, fill):
    pdf.set_font("Arial", '', 12)
    pdf.set_fill_color(230, 230, 230)  # light grey
    pdf.cell(100, 10, name, border=1, fill=fill)
    pdf.cell(40, 10, str(score), border=1, align='R', fill=fill)
    pdf.ln()

# Read data
df = pd.read_csv('data.csv')

# Calculate stats
average_score = df['Score'].mean()
highest_score = df['Score'].max()
lowest_score = df['Score'].min()

# Create PDF
pdf = PDFReport()
pdf.add_page()

# Add table with striped rows
add_table_header(pdf)
fill = False
for _, row in df.iterrows():
    add_table_row(pdf, row['Name'], row['Score'], fill)
    fill = not fill

# Add summary box
pdf.ln(10)
pdf.set_fill_color(240, 240, 240)
pdf.cell(140, 40, border=1, fill=True)
pdf.set_xy(15, pdf.get_y() - 40)
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "Summary Statistics:", ln=True)
pdf.set_font("Arial", '', 12)
pdf.cell(0, 10, f"Average Score: {average_score:.2f}", ln=True)
pdf.cell(0, 10, f"Highest Score: {highest_score}", ln=True)
pdf.cell(0, 10, f"Lowest Score: {lowest_score}", ln=True)

# Save PDF
pdf.output("improved_report.pdf")
print("Improved PDF report generated: improved_report.pdf")
