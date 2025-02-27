import streamlit as st
import pandas as pd 
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("♻ DataSweeper Sterling Integrator by Ad_Bhai")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Ensure df is properly defined before displaying it
        if "df" in locals():
            st.write(f"🔍 Preview of {file.name}")
            st.dataframe(df.head())
        else:
            st.error("Error loading file. Please upload a valid CSV or Excel file.")

        # Data cleaning options
        st.subheader("© Data Cleaning Options")

        if st.checkbox(f"Clean data for {file.name}", key=f"clean_{file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates in {file.name}", key=f"dup_{file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}", key=f"fill_{file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled")

        # Column selection
        st.subheader("🔘 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns, key=f"cols_{file.name}")

        if columns:  # Ensure at least one column is selected
            df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualizations for {file.name}", key=f"viz_{file.name}"): 
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion options
        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"convert_{file.name}")

        if st.button(f"Convert {file.name}", key=f"btn_{file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                buffer.seek(0)  # Move cursor to start
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False)
                    writer.close()  # Ensure data is written properly

                buffer.seek(0)  # Move cursor to start
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # Download button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")
