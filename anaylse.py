import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit app title
st.title("Advanced Spreadsheet Analysis Tool")

# File upload section
uploaded_file = st.file_uploader("Upload a spreadsheet (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Load the file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            import openpyxl
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        # Display preview
        st.write("Preview of the uploaded file:")
        st.dataframe(df.head())

        # Ensure required columns
        required_columns = ["Issues", "Outcomes"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"The uploaded file must contain the following columns: {', '.join(required_columns)}")
            st.stop()

        # Clean and preprocess data
        df["Issues"] = df["Issues"].fillna("none").str.lower()
        df["Outcomes"] = df["Outcomes"].fillna("").str.lower()

        # Analysis
        st.subheader("Analysis Results")

        # Issues analysis
        st.write("**Issues Analysis**")
        issue_counts = df["Issues"].value_counts()
        st.write("Counts by issue category:")
        st.dataframe(issue_counts)

        # Visualize issues
        st.write("Issues Distribution:")
        fig, ax = plt.subplots()
        issue_counts.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        # Outcomes analysis
        st.write("**Outcomes Analysis**")
        failed_students = df[df["Outcomes"].str.contains("failed", na=False)]
        borderline_students = df[df["Outcomes"].str.contains("borderline", na=False)]

        st.write(f"Total students with 'Failed' outcome: {len(failed_students)}")
        st.write(f"Total students with 'Borderline' outcome: {len(borderline_students)}")

        # List of failed or borderline students with non-"none" issues
        critical_cases = df[
            (df["Outcomes"].str.contains("failed|borderline", na=False))
            & (df["Issues"] != "none")
        ]
        st.write("**Critical Cases (Failed/Borderline with Issues):**")
        st.dataframe(critical_cases)

        # Visualize outcomes
        st.write("Outcomes Distribution:")
        outcomes_counts = df["Outcomes"].value_counts()
        fig, ax = plt.subplots()
        outcomes_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a file to begin analysis.")
