import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from fileManagement import listFiles
import streamlit as st
import json

def preprocess_data():
    st.title("Preprocess Data")
    
    csv_files = listFiles()
    if not csv_files:
        st.warning("No CSV files available. Please upload a file first.")
    else:
        selected_file = st.selectbox("Select a CSV file to preprocess:", csv_files)
        
        if selected_file:
            df = pd.read_csv(os.path.join("data", selected_file))
            st.write("### Data Preview:")
            st.dataframe(df.head())
            
            if st.button("Analyze Data"):
                null_counts = df.isnull().sum()
                null_info = pd.DataFrame({"Column": df.columns, "Null Values": null_counts.values})
                st.write("### Null Values per Column:")
                st.dataframe(null_info)
                
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                st.write("### Categorical Columns:")
                st.write(categorical_cols if categorical_cols else "No categorical columns found.")
            
            if st.button("Preprocess Data"):
                label_encoders = {}
                for col in df.columns:
                    if df[col].isnull().sum() > 0:
                        df[col].fillna(df[col].mode()[0], inplace=True) 
                    
                    if df[col].dtype == 'object':
                        le = LabelEncoder()
                        df[col] = le.fit_transform(df[col])
                        label_encoders[col] = {str(k): int(v) for k, v in zip(le.classes_, le.transform(le.classes_))}
                
                preprocessed_folder = "preprocessed"
                os.makedirs(preprocessed_folder, exist_ok=True)
                preprocessed_filename = f"{selected_file}"
                df.to_csv(os.path.join("preprocessed", preprocessed_filename), index=False)
                st.success(f"Preprocessed file saved as {preprocessed_filename}")
                
                mapping_folder = "mapping"
                os.makedirs(mapping_folder, exist_ok=True)
                selected_fileA = selected_file.split(".")
                mapping_file = os.path.join(mapping_folder, f"{selected_fileA[0]}.json")
                with open(mapping_file, "w") as f:
                    json.dump(label_encoders, f, indent=4)
                st.success(f"Label encoding mappings saved in {mapping_file}")