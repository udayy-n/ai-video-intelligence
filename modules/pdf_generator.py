from fpdf import FPDF


def generate_pdf(report):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.set_font(
        "Arial",
        size=11
    )

    report = report.encode(
        "latin-1",
        "replace"
    ).decode(
        "latin-1"
    )

    pdf.multi_cell(
        0,
        8,
        report
    )

    pdf_path = "exports/report.pdf"

    pdf.output(
        pdf_path
    )

    return pdf_path