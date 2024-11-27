import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Moderation Analysis and Comparison Tool")

# Define required columns at the top of the script
required_columns = ["Issues", "Borderline Students", "Failed Students"]

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
                # Process data for both files
                def process_data(df):
                    issues_summary = df["Issues"].apply(
                        lambda x: "No" if pd.isna(x) or str(x).strip().lower() == "none" else "Yes"
                    ).value_counts()
                    total_borderline = df["Borderline Students"].fillna(0).sum()
                    total_failed = df["Failed Students"].fillna(0).sum()
                    return issues_summary, total_borderline, total_failed

                issues_summary1, total_borderline1, total_failed1 = process_data(df1)
                issues_summary2, total_borderline2, total_failed2 = process_data(df2)

                # Display comparison
                st.subheader("Comparison Results")
                comparison_df = pd.DataFrame({
                    "Metric": ["No issues", "Issues", "Total Borderline Students", "Total Failed Students"],
                    "Spreadsheet 1": [
                        issues_summary1.get("No", 0),
                        issues_summary1.get("Yes", 0),
                        int(total_borderline1),
                        int(total_failed1)
                    ],
                    "Spreadsheet 2": [
                        issues_summary2.get("No", 0),
                        issues_summary2.get("Yes", 0),
                        int(total_borderline2),
                        int(total_failed2)
                    ]
                })
                st.dataframe(comparison_df)

                # Visualization
                st.subheader("Visualization")
                st.bar_chart(data=comparison_df.set_index("Metric"))
            else:
                st.error(f"Both files must contain the following columns: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
