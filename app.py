import streamlit as st
import pandas as pd
import joblib

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💼",
    layout="centered"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

/* Hide Streamlit Header/Footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Glass Card */
.glass {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(15px);
    padding: 40px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0px 8px
