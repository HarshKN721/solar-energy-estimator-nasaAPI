import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_csv(data, filename):
    df = pd.DataFrame([data])
    df.to_csv(filename, index=False)

def export_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    text = c.beginText(40, 800)

    for key, value in data.items():
        text.textLine(f"{key}: {value}")

    c.drawText(text)
    c.save()
