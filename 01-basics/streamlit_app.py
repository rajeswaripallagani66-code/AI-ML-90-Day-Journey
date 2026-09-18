import streamlit as st
import joblib
import numpy as np

# load model if you have, else dummy
st.title("Iris Predictor - P1 Project")
st.write("Built with Docker + CI/CD")

sepal_length = st.slider("Sepal Length", 4.0, 8.0, 5.1)
sepal_width = st.slider("Sepal Width", 2.0, 4.5, 3.5)
petal_length = st.slider("Petal Length", 1.0, 7.0, 1.4)
petal_width = st.slider("Petal Width", 0.1, 2.5, 0.2)

if st.button("Predict"):
    st.success(f"Prediction for [{sepal_length}, {sepal_width}, {petal_length}, {petal_width}] -> Setosa (Demo)")
    st.balloons()
    st.toast("Prediction Done!", icon="🎉")