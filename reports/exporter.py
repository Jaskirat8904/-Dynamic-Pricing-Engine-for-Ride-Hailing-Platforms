from fpdf import FPDF


def build_pdf_report(df, title="Dynamic Pricing Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, ln=1, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    if df.empty:
        pdf.cell(0, 8, "No data available.", ln=1)
    else:
        preview = df.head(20)
        for _, row in preview.iterrows():
            line = " | ".join([str(x) for x in row.values[:6]])
            pdf.multi_cell(0, 7, line)

    return pdf.output(dest="S").encode("latin-1")
