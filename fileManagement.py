import streamlit as st
import os

SAVE_DIR = "data"
os.makedirs(SAVE_DIR,exist_ok=True)

def upload_csv():
    uploaded_file = st.file_uploader("Upload a new document (CSV):", type=['csv'])
    if uploaded_file is not None:
        file_path = os.path.join(SAVE_DIR,uploaded_file.name)    
        with open (file_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File Uploaded Successfully")

def listFiles():
    st.subheader("Uploaded Files")
    files = os.listdir(SAVE_DIR)
    if files:
        for file in files:
            col1,col2 = st.columns([4,1])
            col1.write(file)
            if col2.button("delete",key=file):
                os.remove(os.path.join(SAVE_DIR,file))
                st.success(f"Deleted {file}")
                st.rerun()
    else:
        st.info("No files uploaded")
    return files