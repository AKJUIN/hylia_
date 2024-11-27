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
 # Identify modules with and without issues
df['Has Issues'] = df['Issues'].apply(
    lambda x: 'No' if str(x).strip().lower() == 'none' else 'Yes'
)

# Count the number of modules with and without issues
issues_summary_corrected = df['Has Issues'].value_counts()           

            # Analyze 'Outcomes' column for 'failed' and 'borderline'
            outcomes_failed_count = df["Outcomes"].str.lower().str.contains("failed", na=False).sum()
            outcomes_borderline_count = df["Outcomes"].str.lower().str.contains("borderline", na=False).sum()

            # Display results
            st.subheader("Analysis Results")
            st.write("**Issues Analysis:**")
            st.write(f"- Count of 'None' in Issues column: {issues_none_count}")
            st.write(f"- Count of other values in Issues column: {issues_other_count}")

            st.write("**Outcomes Analysis:**")
            st.write(f"- Count of 'Failed' in Outcomes column: {outcomes_failed_count}")
            st.write(f"- Count of 'Borderline' in Outcomes column: {outcomes_borderline_count}")
        else:
            st.error(f"The uploaded file must contain the following columns: {', '.join(required_columns)}")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a file to begin analysis.")
