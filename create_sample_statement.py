from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "sample_statements" / "format_a_example_wealth.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="SmallGray", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#5B6470")))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontSize=11, leading=14, spaceBefore=6, spaceAfter=5, textColor=colors.HexColor("#16324F")))
styles.add(ParagraphStyle(name="Meta", parent=styles["Normal"], fontSize=9, leading=12))


def money(v):
    return f"INR {v:,.2f}"


def make_pdf():
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=17*mm, leftMargin=17*mm, topMargin=15*mm, bottomMargin=15*mm)
    story = []
    story.append(Paragraph("EXAMPLE WEALTH MANAGEMENT", styles["Title"]))
    story.append(Paragraph("Synthetic PMS Portfolio Statement - For software testing only", styles["SmallGray"]))
    story.append(Spacer(1, 8))

    meta = [
        [Paragraph("<b>Provider</b><br/>Example Wealth Management", styles["Meta"]), Paragraph("<b>Strategy</b><br/>Growth Strategy PMS", styles["Meta"])],
        [Paragraph("<b>Client Identifier</b><br/>TEST-CLIENT-001", styles["Meta"]), Paragraph("<b>Statement Period</b><br/>01 Sep 2026 - 30 Sep 2026", styles["Meta"])],
        [Paragraph("<b>Currency</b><br/>INR", styles["Meta"]), Paragraph("<b>Statement Type</b><br/>Portfolio Management Services (PMS)", styles["Meta"])],
    ]
    mt = Table(meta, colWidths=[87*mm, 87*mm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F3F6F9")),
        ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D7DEE7")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(mt)

    story.append(Paragraph("Portfolio Summary", styles["Section"]))
    summary = [
        ["Opening Value", "Additions", "Fees Charged", "Closing Value", "Cash Balance"],
        ["32,000.00", "500.00", "0.00", "32,500.00", "2,500.00"],
    ]
    st = Table(summary, colWidths=[34.8*mm]*5)
    st.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#16324F")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#C7D0DA")),
        ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(st)

    story.append(Paragraph("Holdings", styles["Section"]))
    holdings = [
        ["Security", "ISIN", "Quantity", "Cost (INR)", "Market Value (INR)", "Weight (%)"],
        ["Infosys Ltd", "INE009A01021", "10", "15,000.00", "18,000.00", "60.00"],
        ["Reliance Industries Ltd", "INE002A01018", "5", "12,000.00", "12,000.00", "40.00"],
    ]
    ht = Table(holdings, colWidths=[39*mm, 31*mm, 18*mm, 27*mm, 32*mm, 16*mm], repeatRows=1)
    ht.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#16324F")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 7.5),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#C7D0DA")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(ht)

    story.append(Paragraph("Transactions", styles["Section"]))
    tx = [
        ["Date", "Type", "Security", "Quantity", "Amount (INR)"],
        ["10-Sep-2026", "Dividend", "Infosys Ltd", "-", "500.00"],
    ]
    tt = Table(tx, colWidths=[27*mm, 30*mm, 55*mm, 25*mm, 35*mm])
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#16324F")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#C7D0DA")),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(tt)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Note: This is fabricated test data. It is not an actual investment statement and must not be used for investment decisions.", styles["SmallGray"]))

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
        canvas.line(17*mm, 12*mm, A4[0]-17*mm, 12*mm)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawString(17*mm, 7*mm, "SYNTHETIC TEST DOCUMENT - DO NOT USE FOR INVESTMENT DECISIONS")
        canvas.drawRightString(A4[0]-17*mm, 7*mm, f"Page {_doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Created {OUT}")


if __name__ == "__main__":
    make_pdf()
