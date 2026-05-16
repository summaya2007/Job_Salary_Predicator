import streamlit as st
import pandas as pd
import joblib

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💼",
    layout="wide"
)

# =========================================
# SESSION STATE
# =========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Demo Login
USERNAME = "admin"
PASSWORD = "1234"

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #cfefff;
    font-family: 'Poppins', sans-serif;
}

/* Hide Streamlit Items */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Container */
.main-container {
    padding-top: 30px;
}

/* Card Design */
.card {
    background: white;
    border-radius: 30px;
    padding: 40px;
    height: 700px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.08);
}

/* Title */
.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: black;
    margin-top: 20px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
    margin-bottom: 40px;
}

/* Input Fields */
.stTextInput input,
.stNumberInput input {
    border: none;
    border-bottom: 2px solid #d1d5db;
    border-radius: 0px;
    background-color: transparent;
    font-size: 18px;
}

/* Select Box */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    height: 55px;
    border-radius: 35px;
    border: 2px solid #444;
    background-color: white;
    color: black;
    font-size: 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #bdeaff;
    color: black;
}

/* Blue Button */
.blue-btn button {
    background-color: #bdeaff !important;
}

/* Result Box */
.result-box {
    background-color: #bdeaff;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-top: 25px;
    font-size: 30px;
    font-weight: bold;
}

/* Image */
.image-center {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOGIN PAGE
# =========================================
if not st.session_state.logged_in:

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # =====================================
    # LEFT CARD
    # =====================================
    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="title">Welcome</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Here you log in securely</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '''
            <div class="image-center">
            <img src="https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
            width="220">
            </div>
            ''',
            unsafe_allow_html=True
        )

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Log In"):

            if username == USERNAME and password == PASSWORD:

                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Invalid Username or Password")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================
    # RIGHT CARD
    # =====================================
    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="title">Salary Predictor</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Predict employee salary using ML</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '''
            <div class="image-center">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            width="180">
            </div>
            ''',
            unsafe_allow_html=True
        )

        st.info("""
Demo Login Credentials

Username: admin  
Password: 1234
""")

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# MAIN APP
# =========================================
if st.session_state.logged_in:

    st.title("💼 Salary Prediction App")

    st.write("Predict salary using Machine Learning")

    # LOAD MODEL FILES
    model = joblib.load("salary_prediction_model.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("model_features.pkl")

    # INPUTS
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
        ["Data Scientist", "Software Engineer", "Manager", "Other"]
    )

    education = st.selectbox(
        "Education Level",
        ["Bachelor", "Master", "PhD", "Other"]
    )

    location = st.selectbox(
        "Location",
        ["Bangalore", "Delhi", "Mumbai", "Other"]
    )

    # PREDICT BUTTON
    if st.button("Predict Salary"):

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
            <div class="result-box">
            💰 Predicted Salary <br><br>
            ₹ {round(prediction[0],2)}
            </div>
            ''',
            unsafe_allow_html=True
        )

    # LOGOUT
    if st.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()
