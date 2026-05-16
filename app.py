# =========================================
# BEAUTIFUL MODERN LOGIN UI
# =========================================

import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import joblib

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💼",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* REMOVE STREAMLIT MENU */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1e1b4b);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* LOGIN CARD */
.login-box {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    padding: 40px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 0px 30px rgba(0,0,0,0.4);
}

/* TITLES */
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    background: linear-gradient(to right, #c084fc, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
    font-size: 18px;
}

/* INPUT BOXES */
.stTextInput input {
    background-color: rgba(255,255,255,0.06);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    height: 50px;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(to right, #c026d3, #2563eb);
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    opacity: 0.9;
}

/* PREDICTION CARD */
.pred-card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

/* SUCCESS BOX */
.success-box {
    background: rgba(16,185,129,0.2);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    color: #6ee7b7;
    font-size: 20px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# DATABASE
# =========================================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT,
password TEXT
)
""")

conn.commit()

# =========================================
# HASH PASSWORD
# =========================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================================
# ADD USER
# =========================================
def add_user(username, password):

    cursor.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username, hash_password(password))
    )

    conn.commit()

# =========================================
# LOGIN USER
# =========================================
def login_user(username, password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    data = cursor.fetchone()

    return data

# =========================================
# SESSION
# =========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("💼 Salary Predictor")

menu = st.sidebar.radio(
    "Navigation",
    ["Login", "Signup"]
)

# =========================================
# SIGNUP PAGE
# =========================================
if menu == "Signup" and not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="title">Create Account</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Signup to continue</div>',
            unsafe_allow_html=True
        )

        new_user = st.text_input("Username")

        new_password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Signup"):

            try:
                add_user(new_user, new_password)

                st.success("Account Created Successfully")

            except:
                st.error("Username already exists")

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# LOGIN PAGE
# =========================================
if menu == "Login" and not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.markdown(
            '<div class="title">Welcome Back 👋</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Login to continue</div>',
            unsafe_allow_html=True
        )

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            result = login_user(username, password)

            if result:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()

            else:
                st.error("Invalid Username or Password")

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# MAIN APP
# =========================================
if st.session_state.logged_in:

    st.title("💼 Salary Prediction App")

    st.write(
        f"Welcome, **{st.session_state.username}** 👋"
    )

    model = joblib.load("salary_prediction_model.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("model_features.pkl")

    col1, col2 = st.columns([2,1])

    with col1:

        experience = st.number_input(
            "Experience (Years)",
            0, 50, 1
        )

        skills = st.number_input(
            "Skills Count",
            0, 50, 5
        )

        certifications = st.number_input(
            "Certifications",
            0, 20, 1
        )

        job_title = st.selectbox(
            "Job Title",
            ["Data Scientist",
             "Software Engineer",
             "Manager",
             "Other"]
        )

        education = st.selectbox(
            "Education Level",
            ["Bachelor",
             "Master",
             "PhD",
             "Other"]
        )

        location = st.selectbox(
            "Location",
            ["Bangalore",
             "Delhi",
             "Mumbai",
             "Other"]
        )

        predict = st.button("Predict Salary")

    with col2:

        st.markdown(
            '<div class="pred-card">',
            unsafe_allow_html=True
        )

        st.subheader("Prediction Result")

        if predict:

            input_data = pd.DataFrame({
                "Experience": [experience],
                "Skills": [skills],
                "Certifications": [certifications],
                "Job_Title": [job_title],
                "Education_Level": [education],
                "Location": [location]
            })

            input_data = pd.get_dummies(input_data)

            input_data = input_data.reindex(
                columns=columns,
                fill_value=0
            )

            input_scaled = scaler.transform(input_data)

            prediction = model.predict(input_scaled)

            st.markdown(
                f'''
                <div class="success-box">
                ₹ {round(prediction[0],2)}
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()
