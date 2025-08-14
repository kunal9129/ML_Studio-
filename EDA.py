import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os
import pickle
from fileManagement import listFiles

def model_EDA():
    st.set_page_config(page_title="Auto EDA Tool", layout="wide")
st.title("📊 Automated EDA with BoxPlots")
st.markdown("Upload a CSV file, and we'll generate boxplots for all numeric columns!")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Show raw data
    st.subheader("📂 Data Preview")
    st.dataframe(df.head())

    # Auto-detect numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if not numeric_cols:
        st.warning("No numeric columns found for boxplots!")
    else:
        st.success(f"Detected numeric columns: `{', '.join(numeric_cols)}`")

        # Let user select columns (or plot all)
        st.subheader("📦 BoxPlot Generator")
        selected_cols = st.multiselect(
            "Select columns for boxplots (default: all)", 
            numeric_cols, 
            default=numeric_cols
        )

        # Generate boxplots
        if selected_cols:
            st.write("### BoxPlots")
            cols_per_row = 2  # Adjust layout
            num_plots = len(selected_cols)
            num_rows = (num_plots + cols_per_row - 1) // cols_per_row
            
            for i in range(num_rows):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i * cols_per_row + j
                    if idx < num_plots:
                        with cols[j]:
                            fig, ax = plt.subplots()
                            sns.boxplot(x=df[selected_cols[idx]], ax=ax)
                            ax.set_title(f"Boxplot of {selected_cols[idx]}")
                            st.pyplot(fig)
        else:
            st.warning("Please select at least one column.")
else:
    st.info("👆 Upload a CSV file to get started.")