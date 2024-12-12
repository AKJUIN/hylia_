import streamlit as st
import pandas as pd
from transformers import pipeline

# Load an NLP model for issue categorization (e.g., sentiment-analysis pipeline)
@st.cache_resource
def load_nlp_model():
    return pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

nlp_model = load_nlp_model()

# Streamlit app title
st.title("AI-Enhanced Spreadsheet Analysis and Module Comparison Tool")

# Define required columns
required_columns = ["Module", "Issues", "Borderline Students", "Failed Students"]

# Tabs for functionality
tab1, tab2 = st.tabs(["Analyze a Single Spreadsheet", "Compare Two Spreadsheets"])


with tab1:
    st.header("Analyze a Single Spreadsheet")
    uploaded_file = st.file_uploader("Upload a spreadsheet (Excel or CSV)", type=["xlsx", "csv"])

    if uploaded_file:
        try:
            # Load the uploaded file
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                import openpyxl
                df = pd.read_excel(uploaded_file, engine="openpyxl")

            # Ensure required columns exist
            if all(col in df.columns for col in required_columns):
                # Process and categorize issues using AI
                st.subheader("AI-Powered Issue Categorization")
                df["Issue Category"] = df["Issues"].apply(
                    lambda x: nlp_model(str(x))[0]["label"] if pd.notna(x) and str(x).strip().lower() != "none" else "No Issue"
                )
                st.dataframe(df[["Module", "Issues", "Issue Category"]])

                # Summarize categorized data
                st.subheader("Categorized Issue Summary")
                category_summary = df["Issue Category"].value_counts()
                st.bar_chart(category_summary)

                # Visualizations for borderline and failed students
                st.subheader("Borderline and Failed Students Visualization")
                st.bar_chart(data=pd.DataFrame({
                    "Category": ["Borderline Students", "Failed Students"],
                    "Count": [df["Borderline Students"].sum(), df["Failed Students"].sum()]
                }).set_index("Category"))
            else:
                st.error(f"The uploaded file must contain the following columns: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Tab 2:
with tab2:
    st.header("Compare Two Spreadsheets")
    uploaded_file1 = st.file_uploader("Upload the first spreadsheet (Excel or CSV)", type=["xlsx", "csv"], key="file1")
    uploaded_file2 = st.file_uploader("Upload the second spreadsheet (Excel or CSV)", type=["xlsx", "csv"], key="file2")

    if uploaded_file1 and uploaded_file2:
        try:
            # Load both files
            def load_file(file):
                if file.name.endswith(".csv"):
                    return pd.read_csv(file)
                elif file.name.endswith(".xlsx"):
                    import openpyxl
                    return pd.read_excel(file, engine="openpyxl")

            df1 = load_file(uploaded_file1)
            df2 = load_file(uploaded_file2)

            # Ensure required columns exist
            if all(col in df1.columns for col in required_columns) and all(col in df2.columns for col in required_columns):
                
                df1["Issues"] = df1["Issues"].apply(
                    lambda x: "No" if pd.isna(x) or str(x).strip().lower() == "none" else "Yes"
                )
                df2["Issues"] = df2["Issues"].apply(
                    lambda x: "No" if pd.isna(x) or str(x).strip().lower() == "none" else "Yes"
                )
                df1["Issue Category"] = df1["Issues"].apply(
                    lambda x: nlp_model(str(x))[0]["label"] if x != "No" else "No Issue"
                )
                df2["Issue Category"] = df2["Issues"].apply(
                    lambda x: nlp_model(str(x))[0]["label"] if x != "No" else "No Issue"
                )

                # Merge and compare
                merged_df = pd.merge(
                    df1[["Module", "Issue Category"]].rename(columns={"Issue Category": "Category Spreadsheet 1"}),
                    df2[["Module", "Issue Category"]].rename(columns={"Issue Category": "Category Spreadsheet 2"}),
                    on="Module",
                    how="outer"
                )

                merged_df["Comparison"] = merged_df.apply(
                    lambda row: "Match" if row["Category Spreadsheet 1"] == row["Category Spreadsheet 2"] else "Mismatch",
                    axis=1
                )

                # Display comparison results
                st.subheader("Module-by-Module AI Comparison")
                st.dataframe(merged_df)

                # Summary of matches and mismatches
                match_count = (merged_df["Comparison"] == "Match").sum()
                mismatch_count = (merged_df["Comparison"] == "Mismatch").sum()

                st.write(f"**Number of Matches:** {match_count}")
                st.write(f"**Number of Mismatches:** {mismatch_count}")

                # Visualization of matches and mismatches
                st.bar_chart(data=pd.DataFrame({
                    "Category": ["Matches", "Mismatches"],
                    "Count": [match_count, mismatch_count]
                }).set_index("Category"))
            else:
                st.error(f"Both files must contain the following columns: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
