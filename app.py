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
    box-shadow: 0px 8px 32px rgba(0,0,0,0.2);
    margin-top: 40px;
}

/* Title */
.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: white;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #f1f5f9;
    margin-bottom: 30px;
    font-size: 18px;
}

/* Inputs */
.stTextInput input,
.stNumberInput input {
    background-color: rgba(255,255,255,0.2);
    color: white;
    border-radius: 12px;
    border: none;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.2);
    border-radius: 12px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    opacity: 0.9;
}

/* Result Box */
.result-box {
    background: rgba(255,255,255,0.2);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-top: 25px;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOGIN SESSION
# =====================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

USERNAME = "admin"
PASSWORD = "1234"

# =====================================
# LOGIN PAGE
# =====================================
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.markdown(
            '<div class="title">💼 Salary Predictor</div>',
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

            if username == USERNAME and password == PASSWORD:

                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Invalid Username or Password")

        st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# MAIN APP
# =====================================
if st.session_state.logged_in:

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">💼 Salary Prediction App</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Predict employee salary using ML model</div>',
        unsafe_allow_html=True
    )

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

    # PREDICTION
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

    st.markdown('</div>', unsafe_allow_html=True)
