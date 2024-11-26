import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Spreadsheet Analysis Tool")

# File upload section
uploaded_file = st.file_uploader("Upload a spreadsheet (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Determine file type and load into a DataFrame
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            # Import openpyxl only if needed
            try:
                import openpyxl
            except ImportError:
                st.error(
                    "Missing optional dependency 'openpyxl'. Please install it using 'pip install openpyxl'."
                )
                st.stop()
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            st.stop()

        # Display the first few rows of the uploaded file
        st.write("Preview of the uploaded file:")
        st.dataframe(df.head())

        # Ensure required columns exist
        required_columns = ["Issues", "Outcomes"]
        if all(col in df.columns for col in required_columns):
            # Analyze 'Issues' column
            issues_none_count = df["Issues"].str.lower().str.contains("none", na=False).sum()
            issues_other_count = df["Issues"].notna().sum() - issues_none_count

            # Analyze 'Outcomes' column for 'failed' and
