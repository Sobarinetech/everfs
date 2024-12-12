import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph

# Function to create PDF factsheet
def generate_factsheet(data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Add Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Fund Factsheet")

    # Add Fund Information
    c.setFont("Helvetica", 12)
    y_position = height - 100
    for col in data.columns:
        c.drawString(50, y_position, f"{col}: {data[col][0]}")
        y_position -= 20

    # Add Placeholder for Table
    y_position -= 30
    c.drawString(50, y_position, "Performance Data:")

    # Draw Table
    y_position -= 30
    performance_data = [data.columns.tolist()] + data.values.tolist()
    table = Table(performance_data, colWidths=[150, 150, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Create Table Flowable
    table.wrapOn(c, 50, y_position)
    table.drawOn(c, 50, y_position)

    # Save PDF
    c.save()

# Streamlit App
st.title("Fund Factsheet Generator")
st.markdown("Upload an Excel file with fund data to generate a professional factsheet.")

# File Upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
if uploaded_file:
    # Read Excel Data
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)

    # Generate Factsheet Button
    if st.button("Generate Factsheet"):
        with st.spinner("Generating factsheet..."):
            output_path = "factsheet.pdf"
            generate_factsheet(df, output_path)
            st.success("Factsheet generated successfully!")

        # Provide Download Link
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download Factsheet",
                data=file,
                file_name="factsheet.pdf",
                mime="application/pdf",
            )
