import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Spreadsheet Analysis and Module Comparison Tool")

# Define required columns at the top of the script
required_columns = ["Module", "Issues", "Borderline Students", "Failed Students"]

# Tabs for functionality
tab1, tab2 = st.tabs(["Analyze a Single Spreadsheet", "Compare Two Spreadsheets"])

# Tab 1: Single spreadsheet analysis
with tab1:
    st.header("Analyze a Single Spreadsheet")
    uploaded_file = st.file_uploader("Upload a spreadsheet (Excel or CSV)", type=["xlsx", "csv"])

    if uploaded_file:
        try:
            # Determine file type and load into a DataFrame
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                import openpyxl
                df = pd.read_excel(uploaded_file, engine="openpyxl")

            # Ensure required columns exist
            if all(col in df.columns for col in required_columns):
                # Process data
                issues_summary = df["Issues"].apply(
                    lambda x: "No" if pd.isna(x) or str(x).strip().lower() == "none" else "Yes"
                ).value_counts()
                total_borderline = df["Borderline Students"].fillna(0).sum()
                total_failed = df["Failed Students"].fillna(0).sum()

                # Display results
                st.subheader("Moderation Analysis")
                st.write(f"**No issues reported:** {issues_summary.get('No', 0)}")
                st.write(f"**Issues reported:** {issues_summary.get('Yes', 0)}")
                st.write(f"**Total Borderline Students:** {int(total_borderline)}")
                st.write(f"**Total Failed Students:** {int(total_failed)}")

                # Visualization
                st.subheader("Visualization")
                st.bar_chart(data=pd.DataFrame({
                    "Category": ["No issues", "Issues"],
                    "Count": [issues_summary.get("No", 0), issues_summary.get("Yes", 0)]
                }).set_index("Category"))
            else:
                st.error(f"The uploaded file must contain the following columns: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Tab 2: Compare two spreadsheets
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
                # Standardize issues column to "Yes"/"No" for consistency
                df1["Issues"] = df1["Issues"].apply(
                    lambda x: "No" if pd.isna(x) or str(x).strip().lower() == "none" else "Yes"
                )
                df2["Issues"] = df2["Issues"].apply(
                    lambda x: "No" if pd.isna(x) or str(x).strip().lower() == "none" else "Yes"
                )

                # Merge data for module-by-module comparison
                merged_df = pd.merge(
                    df1[["Module", "Issues"]].rename(columns={"Issues": "Issues in Spreadsheet 1"}),
                    df2[["Module", "Issues"]].rename(columns={"Issues": "Issues in Spreadsheet 2"}),
                    on="Module",
                    how="outer"
                )

                # Determine if issues match for each module
                merged_df["Issue Comparison"] = merged_df.apply(
                    lambda row: "Match" if row["Issues in Spreadsheet 1"] == row["Issues in Spreadsheet 2"]
                    else "Mismatch",
                    axis=1
                )

                # Display results
                st.subheader("Module-by-Module Issue Comparison")
                st.dataframe(merged_df)

                # Summary of matches and mismatches
                match_count = (merged_df["Issue Comparison"] == "Match").sum()
                mismatch_count = (merged_df["Issue Comparison"] == "Mismatch").sum()

                st.write(f"**Number of Matches:** {match_count}")
                st.write(f"**Number of Mismatches:** {mismatch_count}")

                # Visualization of matches and mismatches
                st.subheader("Match vs. Mismatch Visualization")
                st.bar_chart(data=pd.DataFrame({
                    "Category": ["Matches", "Mismatches"],
                    "Count": [match_count, mismatch_count]
                }).set_index("Category"))
            else:
                st.error(f"Both files must contain the following columns: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
