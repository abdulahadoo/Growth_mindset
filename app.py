import streamlit as st
import pandas as pd 
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper",layout="wide")

#custom Css
st.markdown(
             """
                 <style>
                 .stApp{
                         background-color: blcak;
                         color:white;
                       }
                  </style>    
             """,
             unsafe_allow_html= True
)
#Title and discription
st.title(" ♻ Datasweeper Sterling integrator by Ad_Bhai")
st.write("Transform your file between CVS and Excel formats with build-in data cleaning and visualization Creating the project for Quarter 3")

#File uploader
uploaded_file = st.file_uploader("upload your files (accepts CSV or Excel):" ,type=["cvs","xlsx"], accept_multiple_files=(True))
if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

#File details
st.write("🔍 Preview the head of the DataFrame")
st.dataframe(df.head())
                

#data cleaning
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

st.subheader("🔘 Select Colums to Keep")
columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
df = df[columns]

#data visualzation

st.subheader("📊 Data Visualization")
if st.checkbox(f"Show visualizations for {file.name}"): 
   st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])


#conversion option

st.subheader("🔁 Conversion Options")
conversion_type = st.radio(f"Convert {file.name} to:", ["CSV" , "Excel"], key=file.name)

if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0) 

# download button
st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )  
#success
st.success("🎉 All files processed successfully")   
