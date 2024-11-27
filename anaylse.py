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

        # Ensure required columns exist
        required_columns = ["Issues", "Borderline Students", "Failed Students"]
        if all(col in df.columns for col in required_columns):
            # Identify modules with and without issues
            df['Has Issues'] = df['Issues'].apply(
                lambda x: 'No' if pd.isna(x) or str(x).strip().lower() == 'none' else 'Yes'
            )

            # Count the number of modules with and without issues
            issues_summary_corrected = df['Has Issues'].value_counts()

            # Calculate total borderline and failed students
            total_borderline_students = df["Borderline Students"].fillna(0).sum()
            total_failed_students = df["Failed Students"].fillna(0).sum()

            # Display results
            st.subheader("Moderation Analysis")
            st.write("**Summary of Moderation Issues:**")
            st.write(f"- Count of 'No' (no issues): {issues_summary_corrected.get('No', 0)}")
            st.write(f"- Count of 'Yes' (issues present): {issues_summary_corrected.get('Yes', 0)}")

            st.write("**Borderline and Fails:**")
            st.write(f"- Total Borderline Students: {int(total_borderline_students)}")
            st.write(f"- Total Failed Students: {int(total_failed_students)}")

            # Visualization for issues
            st.subheader("Visualization")
            st.write("**Proportion of Modules With and Without Issues:**")

            # Create a DataFrame for visualization
            issues_summary_df = issues_summary_corrected.reset_index()
            issues_summary_df.columns = ['Has Issues', 'Count']

            # Use Streamlit's bar chart
            st.bar_chart(data=issues_summary_df.set_index('Has Issues'))

        else:
            st.error(f"The uploaded file must contain the following columns: {', '.join(required_columns)}")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a file to begin analysis.")
