import streamlit as st
from fileManagement import upload_csv,listFiles
from preprocessData import preprocess_data
from modelTraining import model_training
from EDA import model_EDA

st.set_page_config(
                   page_title="ML Automation",
                   layout="wide",
                   page_icon="C:\Kunal\ML_Studio\logo.png",
                   initial_sidebar_state= "expanded"
                )

st.sidebar.image('C:\Kunal\ML_Studio\logo.png')
page = st.sidebar.selectbox('Select an option:', ['File Management', 'Preprocess Data',"Model Training"])

if page == 'File Management':
    st.title("File Management System")
    upload_csv()
    listFiles()

elif page == "Preprocess Data":
    preprocess_data()

elif page == "Model Training":
    model_training()