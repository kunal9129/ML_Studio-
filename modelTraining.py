import streamlit as st
import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error

def model_training():
    st.title("Model Training")
    
    preprocessed_files = [f for f in os.listdir("preprocessed") if f.endswith(".csv")]
    if not preprocessed_files:
        st.warning("No preprocessed files available. Please preprocess a dataset first.")
        return
    
    selected_file = st.selectbox("Select a preprocessed CSV file:", preprocessed_files)
    if not selected_file:
        return
    
    df = pd.read_csv(os.path.join("preprocessed", selected_file))
    y_column = st.selectbox("Select the target (Y) column:", df.columns)
    problem_type = st.selectbox("Select problem type:", ["Classification", "Regression"])
    
    if y_column and problem_type:
        X = df.drop(columns=[y_column])
        y = df[y_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        models = {}
        if problem_type == "Classification":
            models = {
                "KNN": KNeighborsClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier()
            }
        elif problem_type == "Regression":
            models = {"Linear Regression": LinearRegression()}
        
        accuracies = {}
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            if problem_type == "Classification":
                accuracies[model_name] = accuracy_score(y_test, y_pred)
            else:
                accuracies[model_name] = mean_squared_error(y_test, y_pred)
        
        st.write("### Model Performance")
        for model_name, score in accuracies.items():
            st.write(f"{model_name}: {score:.4f}")
        
        chosen_model_name = st.selectbox("Select model to save:", list(models.keys()))
        if st.button("Save Model"):
            chosen_model = models[chosen_model_name]
            selected_fileA = selected_file.split(".")
            model_filename = os.path.join("models", f"{selected_fileA[0]}.pkl")
            with open(model_filename, "wb") as f:
                pickle.dump(chosen_model, f)
            st.success(f"Model saved as {model_filename}")